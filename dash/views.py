```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            account = get_object_or_404(Account, id=account_id, owner=request.user)
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return redirect('account_detail', account_id=account.id)
        else:
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.owner = request.user
                new_account.save()
                return redirect('account_list')

    elif request.method == 'GET':
        form = AccountForm(instance=get_object_or_404(Account, id=account_id, owner=request.user)) if account_id else AccountForm()
    
    return render(request, 'bank/manage_account.html', {'form': form, 'account_id': account_id})

@login_required
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

@login_required
def create_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=201)

    else:
        form = TransactionForm()

    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})
```