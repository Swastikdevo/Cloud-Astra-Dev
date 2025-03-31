```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_dashboard(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    if request.method == 'POST':
        # Handle deposit
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                # Log transaction
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='deposit')
                return redirect('account_dashboard')
                
        # Handle withdrawal
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    # Log transaction
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='withdrawal')
                    return redirect('account_dashboard')
        
        # Handle transfer
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_account_number = transfer_form.cleaned_data['recipient_account_number']
                amount = transfer_form.cleaned_data['amount']
                recipient_account = Account.objects.get(account_number=recipient_account_number)
                
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    # Log transactions
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in')
                    return redirect('account_dashboard')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    context = {
        'user_account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'account/dashboard.html', context)
```