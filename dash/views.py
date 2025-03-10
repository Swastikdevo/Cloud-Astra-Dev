```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
import json

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user).values('id', 'balance', 'account_number')
        return render(request, 'bank/accounts.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create_account':
            account_number = data.get('account_number')
            initial_balance = data.get('initial_balance', 0)
            new_account = Account.objects.create(
                user=request.user,
                account_number=account_number,
                balance=initial_balance
            )
            return JsonResponse({'status': 'success', 'account_id': new_account.id})

        elif action == 'make_transaction':
            account_id = data.get('account_id')
            amount = data.get('amount')
            transaction_type = data.get('transaction_type')  # 'deposit' or 'withdraw'

            account = Account.objects.get(id=account_id, user=request.user)
            if transaction_type == 'deposit':
                account.balance += amount
            elif transaction_type == 'withdraw':
                if account.balance >= amount:
                    account.balance -= amount
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)

            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)
```