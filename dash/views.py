```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.core.exceptions import ObjectDoesNotExist

@login_required
def manage_account(request, account_id=None):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm(instance=get_object_or_404(Account, id=account_id)) if account_id else AccountForm()

    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
def transaction_view(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'message': 'Transaction successful!', 'transaction_id': transaction.id}, status=200)

    form = TransactionForm()
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    return render(request, 'bank/transaction.html', {
        'form': form,
        'account': account,
        'transactions': transactions
    })

@login_required
def account_summary(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    balance = account.get_balance()
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    return render(request, 'bank/account_summary.html', {
        'account': account,
        'balance': balance,
        'transactions': transactions
    })
```