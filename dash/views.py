```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.db import transaction

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

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def perform_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            with transaction.atomic():
                transaction_obj = transaction_form.save(commit=False)
                account = Account.objects.get(id=transaction_obj.account.id, user=request.user)
                account.balance += transaction_obj.amount
                account.save()
                transaction_obj.save()
                return JsonResponse({'success': True, 'message': 'Transaction successful!'})
    else:
        transaction_form = TransactionForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/transaction.html', {'form': transaction_form, 'accounts': accounts})

@login_required
def account_statement(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_statement.html', {'account': account, 'transactions': transactions})
```