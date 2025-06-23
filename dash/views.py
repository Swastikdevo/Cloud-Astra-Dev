```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Account, Transaction
import json

@csrf_exempt
@require_http_methods(["POST", "GET"])
def account_view(request, account_id=None):
    if request.method == 'GET':
        if account_id:
            account = get_object_or_404(Account, id=account_id)
            return JsonResponse({
                'account_id': account.id,
                'account_holder': account.holder_name,
                'balance': account.balance,
                'status': 'success'
            })
        else:
            accounts = Account.objects.all()
            accounts_data = [
                {
                    'account_id': account.id,
                    'account_holder': account.holder_name,
                    'balance': account.balance
                }
                for account in accounts
            ]
            return JsonResponse({'accounts': accounts_data, 'status': 'success'})
        
    elif request.method == 'POST':
        data = json.loads(request.body)
        account = Account.objects.create(
            holder_name=data['holder_name'],
            initial_balance=data.get('initial_balance', 0)
        )
        return JsonResponse({
            'account_id': account.id,
            'account_holder': account.holder_name,
            'balance': account.balance,
            'status': 'success'
        }, status=201)

@csrf_exempt
@require_http_methods(["POST"])
def transaction_view(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    data = json.loads(request.body)
    
    transaction_type = data.get('transaction_type')
    amount = data.get('amount', 0)

    if transaction_type == 'deposit':
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, transaction_type='deposit', amount=amount)
    elif transaction_type == 'withdrawal':
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, transaction_type='withdrawal', amount=amount)
        else:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid transaction type'}, status=400)
    
    return JsonResponse({
        'account_id': account.id,
        'balance': account.balance,
        'status': 'success'
    })
```