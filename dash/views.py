```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransactionForm, AccountForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully.')
            return redirect('manage_account')
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'account_form': account_form, 'accounts': accounts})

@login_required
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully.')
            return redirect('manage_account')
    else:
        transaction_form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'transaction_form': transaction_form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

@login_required
def api_balance(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    return JsonResponse({'balance': account.balance, 'currency': account.currency})
```