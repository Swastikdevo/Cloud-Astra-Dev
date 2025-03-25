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
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(instance=account)
            return render(request, 'bank/manage_account.html', {'form': form, 'account': account})
        else:
            form = AccountForm()
            return render(request, 'bank/manage_account.html', {'form': form})

    elif request.method == 'POST':
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save()
            return redirect('account_detail', account_id=account.id)
        else:
            return render(request, 'bank/manage_account.html', {'form': form})

@login_required
@csrf_exempt
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account)

    if request.method == 'GET':
        return render(request, 'bank/transaction_history.html', {'transactions': transactions})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
```