```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import BankAccount
import json

@csrf_exempt
@require_http_methods(["POST", "GET"])
def manage_account(request, account_id=None):
    if request.method == "POST":
        data = json.loads(request.body)
        if 'action' in data:
            action = data['action']
            if action == 'create':
                account = BankAccount.objects.create(
                    account_holder=data['account_holder'],
                    initial_balance=data.get('initial_balance', 0)
                )
                return JsonResponse({'message': 'Account created', 'account_id': account.id}, status=201)
            elif action == 'deposit':
                account = get_object_or_404(BankAccount, id=account_id)
                amount = data.get('amount', 0)
                account.balance += amount
                account.save()
                return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})
            elif action == 'withdraw':
                account = get_object_or_404(BankAccount, id=account_id)
                amount = data.get('amount', 0)
                if amount > account.balance:
                    return JsonResponse({'message': 'Insufficient funds'}, status=400)
                account.balance -= amount
                account.save()
                return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})
        return JsonResponse({'message': 'Invalid action'}, status=400)
    
    elif request.method == "GET":
        if account_id:
            account = get_object_or_404(BankAccount, id=account_id)
            return JsonResponse({
                'account_holder': account.account_holder,
                'balance': account.balance
            })
        else:
            accounts = BankAccount.objects.values('id', 'account_holder', 'balance')
            return JsonResponse(list(accounts), safe=False)
    
    return JsonResponse({'message': 'Method not allowed'}, status=405)
```