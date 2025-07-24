```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_view(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.owner = user
            new_account.save()
            return redirect('account_view')  # Redirect to the same view after creating an account
    else:
        form = AccountForm()

    context = {
        'accounts': accounts,
        'form': form,
    }
    
    return render(request, 'bank/account_view.html', context)

@login_required
def transaction_view(request, account_id):
    user = request.user
    account = Account.objects.get(id=account_id, owner=user)
    transactions = Transaction.objects.filter(account=account)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.account = account
            new_transaction.save()
            return redirect('transaction_view', account_id=account_id)
    else:
        form = TransactionForm()

    context = {
        'account': account,
        'transactions': transactions,
        'form': form,
    }

    return render(request, 'bank/transaction_view.html', context)

@login_required
def account_summary(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    total_balance = sum(account.balance for account in accounts)

    context = {
        'accounts': accounts,
        'total_balance': total_balance,
    }

    return render(request, 'bank/account_summary.html', context)

@login_required
def api_balance(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    data = {'account_balances': {account.name: account.balance for account in accounts}}

    return JsonResponse(data)
```