```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == 'GET':
        account = Account.objects.get(id=account_id) if account_id else None
        form = AccountForm(instance=account)
        context = {
            'form': form,
            'account': account
        }
        return render(request, 'manage_account.html', context)

    elif request.method == 'POST':
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save()
            return JsonResponse({'status': 'success', 'account_id': account.id})

        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@login_required
@csrf_exempt
def record_transaction(request, account_id):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=account_id)
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    transactions = Transaction.objects.filter(account_id=account_id)
    return render(request, 'transactions.html', {'transactions': transactions})
```