```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('manage_account')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient balance!')
                return redirect('manage_account')
        
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_username = form.cleaned_data['recipient']
                account = Account.objects.get(user=request.user)
                
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    if account.balance >= amount:
                        account.balance -= amount
                        recipient_account.balance += amount
                        account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer to ' + recipient_username)
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from ' + request.user.username)
                        messages.success(request, 'Transfer successful!')
                    else:
                        messages.error(request, 'Insufficient balance!')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist!')
                return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    
    return render(request, 'bank/manage_account.html', context)
```