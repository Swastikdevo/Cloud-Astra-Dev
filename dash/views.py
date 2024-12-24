```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request, account_id=None):
    """View to create or update a bank account with transaction support."""
    if account_id:
        account = get_object_or_404(Account, id=account_id)
    else:
        account = None

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm(instance=account)

    return render(request, 'accounts/manage_account.html', {'form': form})

@login_required
def make_transaction(request, account_id):
    """View to handle making transactions for an account."""
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = TransactionForm()

    return render(request, 'transactions/make_transaction.html', {'form': form, 'account': account})

@login_required
def account_detail(request, account_id):
    """View to display account details and associated transactions."""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'accounts/account_detail.html', {'account': account, 'transactions': transactions})
```