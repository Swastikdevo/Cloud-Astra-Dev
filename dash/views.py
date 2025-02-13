```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import BankAccount, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm()

    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def make_transaction(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    form = TransactionForm()
    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})

@login_required
def account_summary(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    total_balance = account.balance
    transaction_data = [{'date': txn.date, 'amount': txn.amount, 'description': txn.description} for txn in transactions]

    return render(request, 'bank/account_summary.html', {
        'account': account,
        'transactions': transaction_data,
        'total_balance': total_balance
    })
```