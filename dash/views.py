```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_accounts')

    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def perform_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('manage_accounts')

    else:
        form = TransactionForm()

    return render(request, 'perform_transaction.html', {'form': form, 'account': account})

@login_required
def view_account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    return render(request, 'account_details.html', {'account': account, 'transactions': transactions})
```