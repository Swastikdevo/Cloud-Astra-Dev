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
            account = get_object_or_404(Account, id=account_id, user=request.user)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_list')
    else:
        if account_id:
            account = get_object_or_404(Account, id=account_id, user=request.user)
            form = AccountForm(instance=account)
        else:
            form = AccountForm()

    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
def create_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        form = TransactionForm()

    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_list.html', {'accounts': accounts})
```