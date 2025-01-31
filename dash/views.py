```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'New account created successfully!')
            return redirect('manage_account')
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {
        'account_form': account_form,
        'accounts': accounts,
    })

@login_required
@require_http_methods(["GET", "POST"])
def process_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction processed successfully!')
            return redirect('process_transaction')
    else:
        transaction_form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/process_transaction.html', {
        'transaction_form': transaction_form,
        'transactions': transactions,
    })
```