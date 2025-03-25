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
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

@login_required
@csrf_exempt
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    if request.method == 'GET':
        return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid transaction data'}, status=400)

@login_required
@csrf_exempt
def delete_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == 'DELETE':
        account.delete()
        return JsonResponse({'status': 'success', 'message': 'Account deleted successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
```