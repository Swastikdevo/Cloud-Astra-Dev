```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_management(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_management')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_management.html', {'form': form, 'accounts': accounts})

@login_required
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('account_management')
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

@login_required
def api_balance(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    balance = account.balance
    return JsonResponse({'account_id': account.id, 'balance': balance})
```