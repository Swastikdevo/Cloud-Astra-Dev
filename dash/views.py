```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@require_POST
def deposit(request, account_id):
    account = Account.objects.get(pk=account_id)
    form = DepositForm(request.POST)

    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        messages.success(request, 'Deposit successful!')
    else:
        messages.error(request, 'Invalid deposit amount!')

    return redirect('account_detail', account_id=account.id)

@require_POST
def withdraw(request, account_id):
    account = Account.objects.get(pk=account_id)
    form = WithdrawForm(request.POST)

    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            messages.success(request, 'Withdrawal successful!')
        else:
            messages.error(request, 'Insufficient funds!')
    else:
        messages.error(request, 'Invalid withdrawal amount!')

    return redirect('account_detail', account_id=account.id)

@require_POST
def transfer(request, account_id):
    account = Account.objects.get(pk=account_id)
    form = TransferForm(request.POST)

    if form.is_valid():
        recipient_account_id = form.cleaned_data['recipient_account_id']
        amount = form.cleaned_data['amount']
        recipient_account = Account.objects.get(pk=recipient_account_id)

        if amount <= account.balance:
            account.balance -= amount
            recipient_account.balance += amount
            account.save()
            recipient_account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
            messages.success(request, 'Transfer successful!')
        else:
            messages.error(request, 'Insufficient funds for transfer!')
    else:
        messages.error(request, 'Invalid transfer details!')

    return redirect('account_detail', account_id=account.id)
```