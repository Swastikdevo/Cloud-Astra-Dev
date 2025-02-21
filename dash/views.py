```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
import json

@csrf_exempt
@login_required
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account_management.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create_account':
            account_type = data.get('account_type')
            initial_balance = data.get('initial_balance', 0)
            account = Account.objects.create(user=request.user, account_type=account_type, balance=initial_balance)
            messages.success(request, 'Account created successfully.')
            return JsonResponse({'account_id': account.id})

        elif action == 'deposit':
            account_id = data.get('account_id')
            amount = data.get('amount')
            account = Account.objects.get(id=account_id, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, 'Deposit successful.')
            return JsonResponse({'new_balance': account.balance})

        elif action == 'withdraw':
            account_id = data.get('account_id')
            amount = data.get('amount')
            account = Account.objects.get(id=account_id, user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                messages.success(request, 'Withdrawal successful.')
                return JsonResponse({'new_balance': account.balance})
            else:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)

        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
```