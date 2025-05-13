```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def deposit(request, account_id):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=account_id, owner=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return redirect('bank:dashboard')
    return HttpResponse('Invalid deposit', status=400)

@login_required
@require_POST
def withdraw(request, account_id):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=account_id, owner=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return redirect('bank:dashboard')
        return HttpResponse('Insufficient balance', status=400)
    return HttpResponse('Invalid withdrawal', status=400)

@login_required
@require_POST
def transfer(request, account_id):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        target_account_id = form.cleaned_data['target_account_id']
        account = Account.objects.get(id=account_id, owner=request.user)
        target_account = Account.objects.get(id=target_account_id)
        if account.balance >= amount:
            account.balance -= amount
            target_account.balance += amount
            account.save()
            target_account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
            return redirect('bank:dashboard')
        return HttpResponse('Insufficient balance', status=400)
    return HttpResponse('Invalid transfer', status=400)
```