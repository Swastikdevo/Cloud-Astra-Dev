```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
import json

@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == 'GET':
        if account_id:
            account = Account.objects.get(id=account_id)
            return JsonResponse({'account_number': account.account_number, 'balance': account.balance})
        else:
            accounts = Account.objects.all().values('id', 'account_number', 'balance')
            return JsonResponse(list(accounts), safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        if 'action' in data:
            if data['action'] == 'create':
                new_account = Account.objects.create(account_number=data['account_number'], balance=data['initial_balance'])
                return JsonResponse({'success': True, 'account_id': new_account.id})

            elif data['action'] == 'deposit' and account_id:
                amount = data.get('amount', 0)
                account = Account.objects.get(id=account_id)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'success': True, 'new_balance': account.balance})

            elif data['action'] == 'withdraw' and account_id:
                amount = data.get('amount', 0)
                account = Account.objects.get(id=account_id)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return JsonResponse({'success': True, 'new_balance': account.balance})
                else:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds'})

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
```