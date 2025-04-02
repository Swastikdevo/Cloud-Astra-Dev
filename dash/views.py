```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.contrib import messages

@login_required
def bank_management_view(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                transfer_amount = form.cleaned_data['amount']
                recipient_account = form.cleaned_data['recipient_account']
                sender_account = Account.objects.get(owner=request.user)
                
                if sender_account.balance >= transfer_amount:
                    sender_account.balance -= transfer_amount
                    recipient_account.balance += transfer_amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(
                        account=sender_account,
                        transaction_type='Transfer',
                        amount=transfer_amount,
                        recipient=recipient_account.owner.username
                    )
                    messages.success(request, f'Transferred ${transfer_amount} to {recipient_account.owner.username}.')
                else:
                    messages.error(request, 'Insufficient funds for transfer.')

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                deposit_amount = form.cleaned_data['amount']
                account = Account.objects.get(owner=request.user)
                account.balance += deposit_amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    transaction_type='Deposit',
                    amount=deposit_amount
                )
                messages.success(request, f'Deposited ${deposit_amount} to your account.')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                withdraw_amount = form.cleaned_data['amount']
                account = Account.objects.get(owner=request.user)
                
                if account.balance >= withdraw_amount:
                    account.balance -= withdraw_amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        transaction_type='Withdraw',
                        amount=withdraw_amount
                    )
                    messages.success(request, f'Withdrew ${withdraw_amount} from your account.')
                else:
                    messages.error(request, 'Insufficient funds for withdrawal.')

    balance = Account.objects.get(owner=request.user).balance
    return render(request, 'bank_management.html', {'balance': balance, 'transfer_form': TransferForm(), 
                                                    'deposit_form': DepositForm(), 'withdraw_form': WithdrawForm()})
```