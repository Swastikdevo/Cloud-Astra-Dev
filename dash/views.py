```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed!')
            return redirect('manage_account')
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})

@login_required
def view_transactions(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/view_transactions.html', {'transactions': transactions, 'account': account})
```