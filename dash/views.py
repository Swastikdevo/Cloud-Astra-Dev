```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
def deposit(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, 'Deposit was successful!')
            return redirect('bank:bank_dashboard')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                messages.success(request, 'Withdrawal was successful!')
                return redirect('bank:bank_dashboard')
            else:
                messages.error(request, 'Insufficient funds!')
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            to_account_id = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            to_account = Account.objects.get(id=to_account_id)
            if amount <= account.balance:
                account.balance -= amount
                to_account.balance += amount
                account.save()
                to_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                messages.success(request, 'Transfer was successful!')
                return redirect('bank:bank_dashboard')
            else:
                messages.error(request, 'Insufficient funds for transfer!')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form, 'account': account})
```