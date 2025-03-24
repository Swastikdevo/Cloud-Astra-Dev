```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
import json

@login_required
@csrf_exempt
def manage_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'GET':
        transactions = Transaction.objects.filter(account=account).order_by('-date')
        return render(request, 'accounts/manage_account.html', {'account': account, 'transactions': transactions})

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'deposit':
            amount = data.get('amount', 0)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'status': 'success', 'message': 'Deposit successful.', 'new_balance': account.balance})

        elif action == 'withdraw':
            amount = data.get('amount', 0)
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='withdraw')
                return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.', 'new_balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'}, status=400)

        elif action == 'transfer':
            target_account_id = data.get('target_account_id')
            target_account = get_object_or_404(Account, id=target_account_id)
            amount = data.get('amount', 0)

            if amount <= account.balance:
                account.balance -= amount
                target_account.balance += amount
                account.save()
                target_account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='transfer', target_account=target_account)
                Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer', source_account=account)
                return JsonResponse({'status': 'success', 'message': 'Transfer successful.', 'new_balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance for transfer.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
```