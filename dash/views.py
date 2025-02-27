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
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account/manage.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create':
            account_type = data.get('account_type')
            balance = data.get('balance', 0)
            new_account = Account.objects.create(user=request.user, account_type=account_type, balance=balance)
            messages.success(request, f'Account {new_account.account_type} created successfully.')
            return JsonResponse({'status': 'success', 'account_id': new_account.id})

        elif action == 'deposit':
            account_id = data.get('account_id')
            amount = data.get('amount', 0)
            account = Account.objects.get(id=account_id, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, 'Deposit successful.')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif action == 'withdraw':
            account_id = data.get('account_id')
            amount = data.get('amount', 0)
            account = Account.objects.get(id=account_id, user=request.user)
            if amount > account.balance:
                messages.error(request, 'Insufficient balance.')
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'})
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            messages.success(request, 'Withdrawal successful.')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
```