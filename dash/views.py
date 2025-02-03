```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        # Create a new account
        form = AccountForm(json.loads(request.body))
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'}, status=201)
        return JsonResponse({'status': 'error', 'message': 'Invalid data!'}, status=400)

    elif request.method == 'GET':
        # Retrieve accounts for the logged-in user
        accounts = Account.objects.filter(user=request.user)
        accounts_data = [{'id': account.id, 'balance': account.balance} for account in accounts]
        return JsonResponse({'status': 'success', 'accounts': accounts_data}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed!'}, status=405)

@login_required
@csrf_exempt
def make_transaction(request):
    if request.method == 'POST':
        # Process a new transaction
        form = TransactionForm(json.loads(request.body))
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'}, status=201)
        return JsonResponse({'status': 'error', 'message': 'Invalid transaction data!'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed!'}, status=405)
```