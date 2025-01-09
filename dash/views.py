```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import TransactionForm, AccountForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')
    
    return render(request, 'bank/account_dashboard.html', {
        'accounts': user_accounts,
        'transactions': transactions,
    })

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('account_dashboard')
    else:
        form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('account_dashboard')
    else:
        form = TransactionForm()
    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'bank/transaction_history.html', {
        'account': account,
        'transactions': transactions
    })
```