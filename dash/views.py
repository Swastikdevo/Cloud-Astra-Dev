```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_management(request):
    user_accounts = Account.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.owner = request.user
            new_account.save()
            messages.success(request, 'New account created successfully!')
            return redirect('account_management')
    else:
        form = AccountForm()

    context = {
        'user_accounts': user_accounts,
        'form': form,
    }
    return render(request, 'bank/account_management.html', context)

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('make_transaction')
    else:
        form = TransactionForm()

    context = {
        'form': form,
    }
    return render(request, 'bank/make_transaction.html', context)

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    context = {
        'transactions': transactions,
    }
    return render(request, 'bank/transaction_history.html', context)
```