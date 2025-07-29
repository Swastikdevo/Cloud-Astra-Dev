```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

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
        messages.success(request, 'Deposit successful!')
        return redirect('bank_dashboard')
    messages.error(request, 'Invalid deposit amount.')
    return redirect('bank_dashboard')

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
            messages.success(request, 'Withdrawal successful!')
        else:
            messages.error(request, 'Insufficient funds.')
    else:
        messages.error(request, 'Invalid withdrawal amount.')
    return redirect('bank_dashboard')

@login_required
@require_POST
def transfer(request, account_id):
    form = TransferForm(request.POST)
    if form.is_valid():
        from_account = Account.objects.get(id=account_id, user=request.user)
        to_account = Account.objects.get(id=form.cleaned_data['to_account_id'], user=request.user)
        amount = form.cleaned_data['amount']
        if from_account.balance >= amount:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
            messages.success(request, 'Transfer successful!')
        else:
            messages.error(request, 'Insufficient funds for transfer.')
    else:
        messages.error(request, 'Invalid transfer amount.')
    return redirect('bank_dashboard')
```