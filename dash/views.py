```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction successfully recorded.')
            return redirect('bank_dashboard')

    else:
        form = TransactionForm()

    context = {
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'bank/dashboard.html', context)

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account successfully created.')
            return redirect('bank_dashboard')
    else:
        form = AccountForm()

    context = {
        'form': form,
    }
    return render(request, 'bank/create_account.html', context)

@login_required
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/account_detail.html', context)
```