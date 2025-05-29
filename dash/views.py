```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    user_accounts = Account.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = AccountForm(request.POST)

        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.owner = request.user
            new_account.save()
            messages.success(request, 'New account created successfully!')
            return redirect('manage_account')
    else:
        form = AccountForm()

    return render(request, 'bank/manage_account.html', {
        'accounts': user_accounts,
        'form': form
    })

@login_required
def view_transactions(request):
    user_transactions = Transaction.objects.filter(account__owner=request.user)

    return render(request, 'bank/view_transactions.html', {
        'transactions': user_transactions
    })

@login_required
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('view_transactions')
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {
        'form': form,
        'account': account
    })
```