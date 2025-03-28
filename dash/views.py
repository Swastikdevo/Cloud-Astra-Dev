```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages
from django.db import transaction

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
    else:
        form = AccountForm()
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def transactions(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                transaction = form.save(commit=False)
                transaction.account = account
                transaction.user = request.user
                transaction.save()
                messages.success(request, 'Transaction recorded successfully!')
                return redirect('transactions', account_id=account.id)
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/transactions.html', {'form': form, 'transactions': transactions, 'account': account})
```