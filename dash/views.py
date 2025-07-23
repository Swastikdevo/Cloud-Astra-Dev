```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
def deposit(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'You have successfully deposited {amount} to your account.')
            return redirect('bank_dashboard')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                messages.success(request, f'You have successfully withdrawn {amount} from your account.')
                return redirect('bank_dashboard')
            else:
                messages.error(request, 'Insufficient funds.')
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == "POST":
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            target_account_id = form.cleaned_data['target_account']
            amount = form.cleaned_data['amount']
            target_account = Account.objects.get(id=target_account_id)

            if account.balance >= amount and target_account != account:
                account.balance -= amount
                target_account.balance += amount
                account.save()
                target_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                messages.success(request, f'You have successfully transferred {amount} to account {target_account_id}.')
                return redirect('bank_dashboard')
            else:
                messages.error(request, 'Insufficient funds or invalid account.')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form, 'account': account})
```