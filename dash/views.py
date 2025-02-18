```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def create_account(request):
    data = json.loads(request.body)
    account_number = data.get('account_number')
    account_holder = data.get('account_holder')
    initial_balance = data.get('initial_balance', 0)

    if not account_number or not account_holder:
        return JsonResponse({'error': 'Account number and holder are required.'}, status=400)

    account = Account.objects.create(
        account_number=account_number,
        account_holder=account_holder,
        balance=initial_balance
    )
    return JsonResponse({'message': 'Account created successfully', 'account_number': account.account_number}, status=201)

@csrf_exempt
@require_POST
def deposit(request, account_number):
    data = json.loads(request.body)
    amount = data.get('amount', 0)

    if amount <= 0:
        return JsonResponse({'error': 'Deposit amount must be greater than zero.'}, status=400)

    try:
        account = Account.objects.get(account_number=account_number)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance}, status=200)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found.'}, status=404)

@csrf_exempt
@require_POST
def withdraw(request, account_number):
    data = json.loads(request.body)
    amount = data.get('amount', 0)

    if amount <= 0:
        return JsonResponse({'error': 'Withdrawal amount must be greater than zero.'}, status=400)

    try:
        account = Account.objects.get(account_number=account_number)
        if account.balance < amount:
            return JsonResponse({'error': 'Insufficient funds.'}, status=400)
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
        return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance}, status=200)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found.'}, status=404)

def get_account_balance(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
        return JsonResponse({'account_number': account.account_number, 'balance': account.balance}, status=200)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found.'}, status=404)
```