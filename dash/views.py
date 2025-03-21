```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request, account_id=None):
    """Handles the creation, updation, and deletion of bank accounts."""
    if request.method == 'POST':
        if account_id:
            account = get_object_or_404(Account, id=account_id, user=request.user)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)
        
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        if account_id:
            account = get_object_or_404(Account, id=account_id, user=request.user)
            form = AccountForm(instance=account)
        else:
            form = AccountForm()

    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
def transaction_history(request, account_id):
    """Displays the transaction history for a specific account."""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

@login_required
def perform_transaction(request, account_id):
    """Handles deposits and withdrawals."""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.user = request.user
            transaction.save()
            if transaction.transaction_type == 'withdrawal':
                account.balance -= transaction.amount
            else:
                account.balance += transaction.amount
            account.save()
            return JsonResponse({'status': 'success', 'balance': account.balance})
    else:
        form = TransactionForm()

    return render(request, 'bank/perform_transaction.html', {'form': form, 'account': account})
```