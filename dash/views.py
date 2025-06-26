```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def bank_dashboard(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = Account.objects.get(user=request.user)
                receiver_account = Account.objects.get(account_number=transfer_form.cleaned_data['receiver_account'])
                amount = transfer_form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='transfer', description=f'Transferred to {receiver_account}')
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='transfer', description=f'Received from {sender_account}')                    
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    return redirect('bank_dashboard')
        
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = Account.objects.get(user=request.user)
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit', description='Deposit made')
                account.save()
                return redirect('bank_dashboard')
        
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = Account.objects.get(user=request.user)
                amount = withdraw_form.cleaned_data['amount']
                
                if account.balance >= amount:
                    account.balance -= amount
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal', description='Withdrawal made')
                    account.save()
                    return redirect('bank_dashboard')

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')

    return render(request, 'bank/dashboard.html', {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    })
```