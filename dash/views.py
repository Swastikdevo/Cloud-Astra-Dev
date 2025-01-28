```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_list')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'account/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'Transaction created successfully!'})
    else:
        form = TransactionForm()

    return render(request, 'transaction/create_transaction.html', {'form': form, 'account': account})

@login_required
def view_transactions(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'transaction/view_transactions.html', {'account': account, 'transactions': transactions})

@login_required
def delete_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        account.delete()
        return redirect('account_list')

    return render(request, 'account/delete_account.html', {'account': account})
```