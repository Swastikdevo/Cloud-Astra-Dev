```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request, account_id=None):
    if account_id:
        account = get_object_or_404(Account, id=account_id, owner=request.user)
    else:
        account = None

    if request.method == 'POST':
        if account:
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)

    else:
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account)

    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

@login_required
def create_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('transaction_history', account_id=account.id)
    else:
        form = TransactionForm()

    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})

@login_required
def ajax_balance_check(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    balance = account.balance
    return JsonResponse({'balance': balance})
```