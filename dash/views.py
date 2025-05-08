```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
import json

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if data.get('action') == 'create_account':
            account_type = data.get('account_type')
            initial_balance = data.get('initial_balance')
            new_account = Account.objects.create(
                user=request.user,
                account_type=account_type,
                balance=initial_balance
            )
            return JsonResponse({'status': 'success', 'account_id': new_account.id})

        elif data.get('action') == 'deposit':
            account_id = data.get('account_id')
            amount = data.get('amount')
            account = Account.objects.get(id=account_id, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif data.get('action') == 'withdraw':
            account_id = data.get('account_id')
            amount = data.get('amount')
            account = Account.objects.get(id=account_id, user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})

    elif request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'manage_account.html', {'accounts': accounts})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
```