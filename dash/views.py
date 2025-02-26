```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank_management/manage_account.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'account_id': account.id})
        
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@csrf_exempt
def transaction_history(request, account_id):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(account__id=account_id, account__user=request.user)
        return render(request, 'bank_management/transaction_history.html', {'transactions': transactions})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=account_id, user=request.user)
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def view_balance(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    return JsonResponse({'account_id': account.id, 'balance': account.balance})
```