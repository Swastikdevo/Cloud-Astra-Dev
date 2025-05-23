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
    try:
        account = Account.objects.get(id=account_id) if account_id else None
    except Account.DoesNotExist:
        account = None

    if request.method == 'POST':
        if account:
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('account_detail', account_id=account.id if account else form.instance.id)

    else:
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form, 'account': account})

@login_required
@csrf_exempt
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

@login_required
@csrf_exempt
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'success': True, 'transaction_id': transaction.id})

    else:
        form = TransactionForm()

    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})
```