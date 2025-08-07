```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank_management/accounts.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create':
            account = Account.objects.create(
                user=request.user,
                account_type=data['account_type'],
                balance=data['initial_balance']
            )
            return JsonResponse({'id': account.id, 'message': 'Account created successfully!'}, status=201)

        elif action == 'deposit':
            account = Account.objects.get(id=data['account_id'], user=request.user)
            amount = data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'message': 'Deposit successful!', 'new_balance': account.balance})

        elif action == 'withdraw':
            account = Account.objects.get(id=data['account_id'], user=request.user)
            amount = data['amount']
            if amount > account.balance:
                return JsonResponse({'message': 'Insufficient funds!'}, status=400)
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
            return JsonResponse({'message': 'Withdrawal successful!', 'new_balance': account.balance})

    return JsonResponse({'message': 'Invalid Request'}, status=400)
```