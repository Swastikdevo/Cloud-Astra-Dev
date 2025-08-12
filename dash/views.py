```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == 'GET':
        account = Account.objects.get(id=account_id) if account_id else None
        form = AccountForm(instance=account)
        return render(request, 'bank/manage_account.html', {'form': form, 'account': account})

    elif request.method == 'POST':
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save()
            return redirect('account_detail', account_id=account.id)

    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
@csrf_exempt
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

@login_required
@csrf_exempt
def make_transaction(request, account_id):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=account_id)
            transaction.save()
            return JsonResponse({'success': True, 'message': 'Transaction successful!'})

    return JsonResponse({'success': False, 'message': 'Invalid transaction data'})
```