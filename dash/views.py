```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_overview')
    else:
        form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def make_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('account_overview')
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

@login_required
def ajax_account_balance(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    balance = account.balance
    return JsonResponse({'balance': balance})
```