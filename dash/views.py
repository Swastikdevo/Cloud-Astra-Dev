```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if account_id:
        account = Account.objects.get(id=account_id)
    else:
        account = None

    if request.method == 'POST':
        if account:
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('account_list')
        else:
            messages.error(request, 'Error updating account. Please correct the errors below.')

    else:
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form, 'account': account})

@require_http_methods(["GET", "POST"])
def record_transaction(request, account_id):
    account = Account.objects.get(id=account_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()

            messages.success(request, 'Transaction recorded successfully!')
            return redirect('account_detail', account_id=account.id)
        else:
            messages.error(request, 'Error recording transaction. Please correct the errors below.')

    else:
        form = TransactionForm()

    return render(request, 'bank/record_transaction.html', {'form': form, 'account': account})
```