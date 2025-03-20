```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
def manage_account(request, account_id=None):
    if account_id:
        account = get_object_or_404(Account, pk=account_id)
    else:
        account = None

    if request.method == 'POST':
        if account:
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                messages.success(request, "Account updated successfully.")
                return redirect('manage_account', account_id=account.id)
        else:
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                messages.success(request, "New account created successfully.")
                return redirect('manage_account', account_id=new_account.id)
    else:
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form, 'account': account})

@login_required
def perform_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction performed successfully.")
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=200)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = TransactionForm()

    return render(request, 'bank/perform_transaction.html', {'form': form})
```