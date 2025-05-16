```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_dashboard(request):
    """Bank dashboard for account overview and transactions."""
    user_accounts = Account.objects.filter(owner=request.user)
    user_transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')

    context = {
        'user_accounts': user_accounts,
        'user_transactions': user_transactions,
    }
    return render(request, 'bank/dashboard.html', context)

@login_required
def deposit(request, account_id):
    """Handle deposits into user accounts."""
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'Deposited ${amount} to {account.account_number}.')
            return redirect('bank_dashboard')
    else:
        form = DepositForm()
    
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    """Handle withdrawals from user accounts."""
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == "POST":
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                messages.success(request, f'Withdrew ${amount} from {account.account_number}.')
                return redirect('bank_dashboard')
            else:
                messages.error(request, 'Insufficient balance.')
    else:
        form = WithdrawalForm()
    
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request):
    """Handle fund transfers between user accounts."""
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = Account.objects.get(id=form.cleaned_data['from_account'], owner=request.user)
            to_account = Account.objects.get(id=form.cleaned_data['to_account'], owner=request.user)
            amount = form.cleaned_data['amount']
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                messages.success(request, f'Transferred ${amount} from {from_account.account_number} to {to_account.account_number}.')
                return redirect('bank_dashboard')
            else:
                messages.error(request, 'Insufficient balance for transfer.')
    else:
        form = TransferForm()
    
    return render(request, 'bank/transfer.html', {'form': form})
```