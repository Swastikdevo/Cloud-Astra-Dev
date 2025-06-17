```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from django.contrib import messages
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_overview(request):
    """Display the account overview for the logged in user."""
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': user_accounts})

@login_required
def deposit(request, account_id):
    """Handle deposits to the user's account."""
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, 'Deposit successful!')
            return redirect('account_overview')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    """Handle withdrawals from the user's account."""
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                messages.error(request, 'Insufficient funds!')
            else:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                messages.success(request, 'Withdrawal successful!')
                return redirect('account_overview')
    else:
        form = WithdrawalForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request, account_id):
    """Handle money transfers between accounts."""
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            target_account_id = form.cleaned_data['target_account_id']
            amount = form.cleaned_data['amount']
            target_account = Account.objects.get(id=target_account_id)

            if amount > account.balance:
                messages.error(request, 'Insufficient funds for transfer!')
            else:
                account.balance -= amount
                target_account.balance += amount
                account.save()
                target_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='transfer_out')
                Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer_in')
                messages.success(request, 'Transfer successful!')
                return redirect('account_overview')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form, 'account': account})
```