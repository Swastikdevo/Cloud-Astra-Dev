```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date_created')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposit of ${amount} successful!')
                return redirect('account_overview')
        
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    messages.success(request, f'Withdrawal of ${amount} successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('account_overview')
        
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_username = transfer_form.cleaned_data['recipient']
                amount = transfer_form.cleaned_data['amount']
                if amount <= account.balance:
                    try:
                        recipient = Account.objects.get(user__username=recipient_username)
                        account.balance -= amount
                        recipient.balance += amount
                        account.save()
                        recipient.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer to ' + recipient_username)
                        messages.success(request, f'Transfer of ${amount} to {recipient_username} successful!')
                    except Account.DoesNotExist:
                        messages.error(request, 'Recipient not found!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('account_overview')
    
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/account_overview.html', context)
```