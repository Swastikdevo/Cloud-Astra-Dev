```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm
from django.contrib import messages

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def deposit(request, account_id):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = Account.objects.get(id=account_id, user=request.user)
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        messages.success(request, 'Deposit successful.')
        return redirect('account_dashboard')
    messages.error(request, 'Deposit failed. Please check the amount.')
    return redirect('account_dashboard')

@login_required
@require_POST
def withdraw(request, account_id):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        account = Account.objects.get(id=account_id, user=request.user)
        amount = form.cleaned_data['amount']
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            messages.success(request, 'Withdrawal successful.')
        else:
            messages.error(request, 'Insufficient balance for this withdrawal.')
    return redirect('account_dashboard')

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        sender_account = Account.objects.get(id=form.cleaned_data['sender_account'], user=request.user)
        receiver_account = Account.objects.get(id=form.cleaned_data['receiver_account'])
        amount = form.cleaned_data['amount']

        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()
            Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='Transfer In')
            messages.success(request, 'Transfer successful.')
        else:
            messages.error(request, 'Insufficient balance for this transfer.')
    return redirect('account_dashboard')
```