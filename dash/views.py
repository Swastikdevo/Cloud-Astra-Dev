```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request, account_id=None):
    if account_id:
        account = Account.objects.get(id=account_id)
    else:
        account = None

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account details updated successfully!' if account else 'New account created successfully!')
            return redirect('manage_account', account_id=form.instance.id)
    else:
        form = AccountForm(instance=account)

    return render(request, 'manage_account.html', {'form': form})

@login_required
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('account_detail', account_id=account.id)
    else:
        form = TransactionForm()

    return render(request, 'make_transaction.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'transaction_history.html', {'account': account, 'transactions': transactions})
```