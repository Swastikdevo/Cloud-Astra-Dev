```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal

@csrf_exempt
@login_required
def bank_operations(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/accounts.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        amount = Decimal(request.POST.get('amount'))

        if action == 'deposit':
            account_id = request.POST.get('account_id')
            with transaction.atomic():
                account = Account.objects.get(id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif action == 'withdraw':
            account_id = request.POST.get('account_id')
            with transaction.atomic():
                account = Account.objects.get(id=account_id, user=request.user)
                if amount > account.balance:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif action == 'transfer':
            from_account_id = request.POST.get('from_account_id')
            to_account_id = request.POST.get('to_account_id')
            with transaction.atomic():
                from_account = Account.objects.get(id=from_account_id, user=request.user)
                to_account = Account.objects.get(id=to_account_id, user=request.user)
                if amount > from_account.balance:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
            return JsonResponse({'status': 'success', 'new_balances': {from_account.id: from_account.balance, to_account.id: to_account.balance}})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
```