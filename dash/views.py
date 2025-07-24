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
def account_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account_management.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create_account':
            account_type = data.get('account_type')
            initial_balance = data.get('initial_balance', 0)

            new_account = Account.objects.create(user=request.user, account_type=account_type, balance=initial_balance)
            messages.success(request, 'Account created successfully!')
            return JsonResponse({'success': True, 'account_id': new_account.id})

        elif action == 'deposit':
            account_id = data.get('account_id')
            amount = data.get('amount', 0)

            try:
                account = Account.objects.get(id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return JsonResponse({'success': True, 'new_balance': account.balance})

            except Account.DoesNotExist:
                messages.error(request, 'Account not found.')
                return JsonResponse({'success': False, 'error': 'Account not found.'})

        elif action == 'withdraw':
            account_id = data.get('account_id')
            amount = data.get('amount', 0)

            try:
                account = Account.objects.get(id=account_id, user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
                    messages.success(request, 'Withdrawal successful!')
                    return JsonResponse({'success': True, 'new_balance': account.balance})
                else:
                    messages.error(request, 'Insufficient funds.')
                    return JsonResponse({'success': False, 'error': 'Insufficient funds.'})

            except Account.DoesNotExist:
                messages.error(request, 'Account not found.')
                return JsonResponse({'success': False, 'error': 'Account not found.'})

        else:
            return JsonResponse({'success': False, 'error': 'Invalid action.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
```