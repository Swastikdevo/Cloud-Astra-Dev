```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_dashboard(request):
    # Fetch user's accounts
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_dashboard')
    else:
        form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def manage_transactions(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('manage_transactions', account_id=account_id)
    else:
        form = TransactionForm()
    
    return render(request, 'bank/manage_transactions.html', {'account': account, 'transactions': transactions, 'form': form})

@login_required
def view_account_statement(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    if not transactions.exists():
        return HttpResponse("No transactions found for this account.")

    return render(request, 'bank/account_statement.html', {'account': account, 'transactions': transactions})
```