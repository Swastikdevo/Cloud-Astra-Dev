```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request, account_id=None):
    if request.method == "POST":
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm(instance=Account.objects.get(id=account_id)) if account_id else AccountForm()

    return render(request, 'manage_account.html', {'form': form})

@login_required
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'success': True, 'message': 'Transaction successful!'})
    else:
        form = TransactionForm()

    return render(request, 'make_transaction.html', {'form': form, 'account': account})

@login_required
def account_summary(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    balance = account.get_balance()
    return render(request, 'account_summary.html', {'account': account, 'transactions': transactions, 'balance': balance})
```