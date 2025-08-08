```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.db import transaction

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': user_accounts})

@login_required
def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            with transaction.atomic():
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return redirect('account_dashboard')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                with transaction.atomic():
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return redirect('account_dashboard')
            else:
                form.add_error('amount', 'Insufficient balance.')
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = get_object_or_404(Account, id=form.cleaned_data['from_account_id'], owner=request.user)
            to_account = get_object_or_404(Account, id=form.cleaned_data['to_account_id'], owner=request.user)
            amount = form.cleaned_data['amount']
            if amount <= from_account.balance:
                with transaction.atomic():
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer_in')
                return redirect('account_dashboard')
            else:
                form.add_error('amount', 'Insufficient balance in the from account.')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form})

@login_required
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})
```