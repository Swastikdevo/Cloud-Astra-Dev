```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Account, Transaction
import json

@csrf_exempt
@require_http_methods(["POST", "GET"])
def account_management(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Create a new account
        if 'action' in data and data['action'] == 'create':
            account = Account.objects.create(
                account_holder=data['account_holder'],
                balance=data['initial_balance']
            )
            return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)

        # Deposit money
        elif 'action' in data and data['action'] == 'deposit':
            account = get_object_or_404(Account, id=data['account_id'])
            amount = data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        # Withdraw money
        elif 'action' in data and data['action'] == 'withdraw':
            account = get_object_or_404(Account, id=data['account_id'])
            amount = data['amount']
            if amount > account.balance:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

    elif request.method == 'GET':
        accounts = Account.objects.all().values('id', 'account_holder', 'balance')
        return JsonResponse(list(accounts), safe=False)
```