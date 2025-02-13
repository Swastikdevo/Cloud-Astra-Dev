```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save()
        return redirect('account_detail', account_id=account.id)
    return render(request, 'bank/create_account.html', {'form': form})

@require_POST
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id)
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()
        return redirect('account_detail', account_id=account.id)
    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})

def account_detail(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})

def dashboard(request):
    accounts = Account.objects.all()
    total_balance = sum(account.balance for account in accounts)
    return render(request, 'bank/dashboard.html', {'accounts': accounts, 'total_balance': total_balance})
```