```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if account_id:
        account = get_object_or_404(Account, id=account_id)
    else:
        account = None

    if request.method == "POST":
        if account:
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully!' if account else 'New account created!')
            return redirect('account_detail', account_id=form.instance.id)
        else:
            messages.error(request, 'Error in form submission.')

    else:
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form, 'account': account})

@login_required
@require_http_methods(["GET", "POST"])
def transact(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('account_detail', account_id=account.id)
        else:
            messages.error(request, 'Error in transaction form.')

    else:
        form = TransactionForm()

    return render(request, 'bank/transact.html', {'form': form, 'account': account})
```