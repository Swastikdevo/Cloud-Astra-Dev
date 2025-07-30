```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully.')
            return redirect('manage_account', account_id=account.id)
    else:
        if account_id:
            account = get_object_or_404(Account, id=account_id, user=request.user)
            form = AccountForm(instance=account)
        else:
            form = AccountForm()

    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
@csrf_exempt
def create_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully.')
            return redirect('account_detail', account_id=account.id)
    else:
        form = TransactionForm()

    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})
```