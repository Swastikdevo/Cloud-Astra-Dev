```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Account, Transaction
import json

@csrf_exempt
@require_http_methods(["POST"])
def create_account(request):
    data = json.loads(request.body)
    account_holder = data.get('account_holder')
    initial_balance = data.get('initial_balance', 0)

    if not account_holder:
        return JsonResponse({'error': 'Account holder name is required.'}, status=400)

    account = Account.objects.create(holder_name=account_holder, balance=initial_balance)
    return JsonResponse({'account_id': account.id, 'holder_name': account.holder_name, 'balance': account.balance}, status=201)

@csrf_exempt
@require_http_methods(["POST"])
def deposit(request, account_id):
    data = json.loads(request.body)
    amount = data.get('amount', 0)

    account = get_object_or_404(Account, id=account_id)
    
    if amount <= 0:
        return JsonResponse({'error': 'Deposit amount must be positive.'}, status=400)

    account.balance += amount
    account.save()

    Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
    
    return JsonResponse({'account_id': account.id, 'new_balance': account.balance}, status=200)

@csrf_exempt
@require_http_methods(["POST"])
def withdraw(request, account_id):
    data = json.loads(request.body)
    amount = data.get('amount', 0)

    account = get_object_or_404(Account, id=account_id)

    if amount <= 0:
        return JsonResponse({'error': 'Withdrawal amount must be positive.'}, status=400)

    if account.balance < amount:
        return JsonResponse({'error': 'Insufficient funds.'}, status=400)

    account.balance -= amount
    account.save()

    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
    
    return JsonResponse({'account_id': account.id, 'new_balance': account.balance}, status=200)

@csrf_exempt
@require_http_methods(["GET"])
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    return JsonResponse({'account_id': account.id, 'holder_name': account.holder_name, 'balance': account.balance}, status=200)
```