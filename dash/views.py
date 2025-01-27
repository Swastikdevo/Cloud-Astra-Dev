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
        return render(request, 'accounts/manage_accounts.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create':
            account_name = data.get('account_name')
            new_account = Account.objects.create(user=request.user, name=account_name)
            messages.success(request, f'Account "{new_account.name}" created successfully.')
            return JsonResponse({'status': 'success', 'account_id': new_account.id})

        elif action == 'delete':
            account_id = data.get('account_id')
            account = Account.objects.get(id=account_id, user=request.user)
            account.delete()
            messages.success(request, f'Account "{account.name}" deleted successfully.')
            return JsonResponse({'status': 'success'})

        elif action == 'transfer':
            from_account_id = data.get('from_account_id')
            to_account_id = data.get('to_account_id')
            amount = data.get('amount')
            from_account = Account.objects.get(id=from_account_id, user=request.user)
            to_account = Account.objects.get(id=to_account_id, user=request.user)

            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                Transaction.objects.create(from_account=from_account, to_account=to_account, amount=amount)
                messages.success(request, f'Transferred ${amount} from "{from_account.name}" to "{to_account.name}" successfully.')
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
```