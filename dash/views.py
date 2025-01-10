```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
import json

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create':
            account = Account.objects.create(
                user=request.user,
                account_type=data.get('account_type'),
                balance=data.get('initial_balance', 0)
            )
            return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)

        elif action == 'transfer':
            source_account = Account.objects.get(id=data.get('source_account_id'))
            target_account = Account.objects.get(id=data.get('target_account_id'))
            amount = data.get('amount')

            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                
                Transaction.objects.create(
                    from_account=source_account,
                    to_account=target_account,
                    amount=amount,
                    user=request.user
                )
                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)

        elif action == 'delete':
            account_id = data.get('account_id')
            Account.objects.filter(id=account_id, user=request.user).delete()
            return JsonResponse({'status': 'success'}, status=204)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
```