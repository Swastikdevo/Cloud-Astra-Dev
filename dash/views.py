```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            account = get_object_or_404(Account, pk=account_id)
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return redirect('account_detail', account_id=account.id)
        else:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save()
                return redirect('account_detail', account_id=account.id)
    else:
        if account_id:
            account = get_object_or_404(Account, pk=account_id)
            form = AccountForm(instance=account)
        else:
            form = AccountForm()

    return render(request, 'manage_account.html', {'form': form})

@login_required
@csrf_exempt
def create_transaction(request, account_id):
    account = get_object_or_404(Account, pk=account_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('transaction_detail', transaction_id=transaction.id)
    else:
        form = TransactionForm()

    return render(request, 'create_transaction.html', {'form': form, 'account': account})

@login_required
def list_transactions(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'list_transactions.html', {'transactions': transactions, 'account': account})
```