```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
import json

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank_management.html', {'accounts': accounts})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')

            if action == 'create_account':
                account_name = data.get('account_name')
                initial_balance = data.get('initial_balance', 0)
                new_account = Account.objects.create(user=request.user, name=account_name, balance=initial_balance)
                return JsonResponse({'message': 'Account created successfully!', 'account_id': new_account.id})

            elif action == 'deposit':
                account_id = data.get('account_id')
                amount = data.get('amount')
                account = Account.objects.get(id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'message': 'Deposit successful!', 'new_balance': account.balance})

            elif action == 'withdraw':
                account_id = data.get('account_id')
                amount = data.get('amount')
                account = Account.objects.get(id=account_id, user=request.user)

                if amount > account.balance:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return JsonResponse({'message': 'Withdrawal successful!', 'new_balance': account.balance})

            else:
                return JsonResponse({'error': 'Invalid action.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
```