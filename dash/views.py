```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            messages.success(request, 'New account created successfully!')
            return redirect('account_detail', account_id=account.id)
        else:
            messages.error(request, 'There was an error creating the account.')
    else:
        form = AccountForm()
    
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': user_accounts})

@login_required
@require_http_methods(["GET", "POST"])
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('account_detail', account_id=account.id)
        else:
            messages.error(request, 'There was an error with the transaction.')
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})
```