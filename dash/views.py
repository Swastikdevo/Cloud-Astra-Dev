```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Account
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def account_management_view(request, account_id=None):
    if request.method == 'GET':
        if account_id:
            account = get_object_or_404(Account, id=account_id)
            return JsonResponse({'account_id': account.id, 'balance': account.balance, 'account_type': account.account_type})
        else:
            accounts = Account.objects.all().values('id', 'balance', 'account_type')
            return JsonResponse(list(accounts), safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'create':
            new_account = Account.objects.create(
                balance=data.get('balance', 0),
                account_type=data.get('account_type', 'savings')
            )
            return JsonResponse({'message': 'Account created successfully', 'account_id': new_account.id}, status=201)

        elif action == 'deposit':
            account = get_object_or_404(Account, id=account_id)
            amount = data.get('amount', 0)
            account.balance += amount
            account.save()
            return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})

        elif action == 'withdraw':
            account = get_object_or_404(Account, id=account_id)
            amount = data.get('amount', 0)
            if amount > account.balance:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
            account.balance -= amount
            account.save()
            return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})

    return JsonResponse({'error': 'Invalid request'}, status=400)
```