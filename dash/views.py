```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

@login_required
def bank_management(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                if account.owner == user:
                    account.balance += amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                    messages.success(request, f'Deposited ${amount} to {account.account_number}.')
                else:
                    messages.error(request, 'Invalid account.')
        
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = withdraw_form.cleaned_data['account']
                amount = withdraw_form.cleaned_data['amount']
                if account.owner == user and account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    messages.success(request, f'Withdrew ${amount} from {account.account_number}.')
                else:
                    messages.error(request, 'Insufficient funds or invalid account.')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                source_account = transfer_form.cleaned_data['source_account']
                destination_account = transfer_form.cleaned_data['destination_account']
                transfer_amount = transfer_form.cleaned_data['amount']
                if source_account.owner == user and source_account.balance >= transfer_amount:
                    source_account.balance -= transfer_amount
                    destination_account.balance += transfer_amount
                    source_account.save()
                    destination_account.save()
                    Transaction.objects.create(account=source_account, amount=transfer_amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=destination_account, amount=transfer_amount, transaction_type='Transfer In')
                    messages.success(request, f'Transferred ${transfer_amount} from {source_account.account_number} to {destination_account.account_number}.')
                else:
                    messages.error(request, 'Insufficient funds or invalid account.')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    return render(request, 'bank_management.html', {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    })
```