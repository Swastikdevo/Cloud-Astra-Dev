```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def banking_dashboard(request):
    # Get the current user's accounts
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]

    context = {
        'accounts': accounts,
        'transactions': transactions,
    }
    return render(request, 'banking/dashboard.html', context)

@login_required
def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()

            # Log the transaction
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('banking:dashboard')
    else:
        form = DepositForm()

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'banking/deposit.html', context)

@login_required
def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()

                # Log the transaction
                Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                return redirect('banking:dashboard')
            else:
                form.add_error('amount', 'Insufficient balance.')
    else:
        form = WithdrawalForm()

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'banking/withdraw.html', context)

@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']

            if amount <= from_account.balance:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()

                # Log the transactions
                Transaction.objects.create(account=from_account, amount=-amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                
                return redirect('banking:dashboard')
            else:
                form.add_error('amount', 'Insufficient balance for transfer.')
    else:
        form = TransferForm(user=request.user)

    context = {
        'form': form,
    }
    return render(request, 'banking/transfer.html', context)
```