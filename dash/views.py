```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, "Account created successfully!")
            return redirect('manage_account')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, "Transaction added successfully!")
            return redirect('transaction_history', account_id=account.id)
    else:
        form = TransactionForm()

    return render(request, 'bank/transaction_history.html', {'form': form, 'transactions': transactions, 'account': account})

@login_required
@require_http_methods(["GET"])
def account_balance(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    balance = account.balance
    return JsonResponse({'account_id': account.id, 'balance': balance})
```