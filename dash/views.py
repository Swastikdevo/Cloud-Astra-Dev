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
def bank_account_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/account_view.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create_account':
            account_name = data.get('name')
            initial_balance = data.get('balance', 0)
            new_account = Account.objects.create(user=request.user, name=account_name, balance=initial_balance)
            messages.success(request, f'Account {new_account.name} created successfully!')
            return JsonResponse({'status': 'success', 'account_id': new_account.id})

        elif action == 'deposit':
            account_id = data.get('account_id')
            amount = data.get('amount')
            account = Account.objects.get(id=account_id, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, f'Deposited {amount} to {account.name}!')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif action == 'withdraw':
            account_id = data.get('account_id')
            amount = data.get('amount')
            account = Account.objects.get(id=account_id, user=request.user)

            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                messages.success(request, f'Withdrew {amount} from {account.name}!')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
            else:
                messages.error(request, 'Insufficient funds for this withdrawal.')
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
```