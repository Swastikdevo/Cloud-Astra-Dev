```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
    else:
        account_form = AccountForm()
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'account_form': account_form, 'accounts': accounts})

@login_required
def perform_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('perform_transaction')
    else:
        transaction_form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'bank/perform_transaction.html', {'transaction_form': transaction_form, 'transactions': transactions})

@login_required
def account_summary(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'bank/account_summary.html', {'account': account, 'transactions': transactions})
    except Account.DoesNotExist:
        messages.error(request, 'Account not found.')
        return redirect('manage_account')
```