```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            # Update existing account
            account = get_object_or_404(Account, id=account_id, owner=request.user)
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account updated successfully!')
                return redirect('account_detail', account_id=account.id)
        else:
            # Create a new account
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.owner = request.user
                new_account.save()
                messages.success(request, 'Account created successfully!')
                return redirect('account_detail', account_id=new_account.id)
    else:
        form = AccountForm(instance=get_object_or_404(Account, id=account_id, owner=request.user) if account_id else None)

    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
def record_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction recorded successfully!')
            return redirect('transaction_history', account_id=account.id)
    else:
        form = TransactionForm()

    return render(request, 'bank/record_transaction.html', {'form': form, 'account': account})

@login_required
def get_account_balance(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    balance = account.get_balance()
    return JsonResponse({'account_id': account.id, 'balance': balance})
```