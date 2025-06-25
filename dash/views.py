```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('view_accounts')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def deposit_money(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = 'Deposit'
            transaction.save()
            account.balance += transaction.amount
            account.save()
            messages.success(request, 'Deposit completed successfully!')
            return redirect('view_accounts')
    else:
        form = TransactionForm()

    return render(request, 'bank/deposit_money.html', {'form': form, 'account': account})

@login_required
def withdraw_money(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid() and form.cleaned_data['amount'] <= account.balance:
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = 'Withdrawal'
            transaction.save()
            account.balance -= transaction.amount
            account.save()
            messages.success(request, 'Withdrawal completed successfully!')
            return redirect('view_accounts')
        elif form.is_valid():
            messages.error(request, 'Insufficient funds for withdrawal.')
    else:
        form = TransactionForm()

    return render(request, 'bank/withdraw_money.html', {'form': form, 'account': account})

@login_required
def view_accounts(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/view_accounts.html', {'accounts': accounts})
```