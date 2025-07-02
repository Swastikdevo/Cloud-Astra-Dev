```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.db import transaction

@login_required
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                transaction = form.save(commit=False)
                transaction.account = account
                transaction.save()
                account.balance += transaction.amount  # Adjust balance for deposit
                account.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        form = TransactionForm()
    
    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})

@login_required
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'bank/account_detail.html', {
        'account': account,
        'transactions': transactions
    })
```