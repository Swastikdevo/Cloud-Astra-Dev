```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages
from django.db import transaction

@login_required
def manage_account(request):
    if request.method == "POST":
        if 'deposit' in request.POST:
            return handle_deposit(request)
        elif 'withdraw' in request.POST:
            return handle_withdraw(request)
        elif 'transfer' in request.POST:
            return handle_transfer(request)

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'accounts': accounts})

@login_required
def handle_deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
        with transaction.atomic():
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, "Successfully deposited.")
        return redirect('manage_account')
    else:
        messages.error(request, "Error in deposit form.")
    return redirect('manage_account')

@login_required
def handle_withdraw(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
        if account.balance >= amount:
            with transaction.atomic():
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                messages.success(request, "Successfully withdrawn.")
        else:
            messages.error(request, "Insufficient funds.")
    else:
        messages.error(request, "Error in withdraw form.")
    return redirect('manage_account')

@login_required
def handle_transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        from_account = Account.objects.get(id=form.cleaned_data['from_account_id'], user=request.user)
        to_account = Account.objects.get(id=form.cleaned_data['to_account_id'])
        
        if from_account.balance >= amount and from_account != to_account:
            with transaction.atomic():
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                messages.success(request, "Successfully transferred.")
        else:
            messages.error(request, "Transfer failed. Check your balance or accounts.")
    else:
        messages.error(request, "Error in transfer form.")
    return redirect('manage_account')
```