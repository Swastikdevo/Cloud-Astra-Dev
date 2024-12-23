```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/accounts.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        form = AccountForm(data)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'message': 'Account created successfully'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@login_required
@csrf_exempt
def transaction_management(request, account_id):
    account = get_object_or_404(Account, pk=account_id, user=request.user)

    if request.method == 'GET':
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'bank/transactions.html', {'transactions': transactions, 'account': account})

    elif request.method == 'POST':
        data = json.loads(request.body)
        form = TransactionForm(data)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'message': 'Transaction recorded successfully'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id, user=request.user)
    if request.method == 'POST':
        account.delete()
        return JsonResponse({'message': 'Account deleted successfully'}, status=204)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
```