```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
import json

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)

        action = data.get('action')
        if action == 'create':
            account_name = data.get('name')
            account_type = data.get('type')
            new_account = Account.objects.create(user=request.user, name=account_name, account_type=account_type)
            return JsonResponse({'status': 'success', 'account_id': new_account.id})
        
        elif action == 'delete':
            account_id = data.get('account_id')
            Account.objects.filter(id=account_id, user=request.user).delete()
            return JsonResponse({'status': 'success', 'message': 'Account deleted'})
        
        elif action == 'view_transaction':
            account_id = data.get('account_id')
            transactions = Transaction.objects.filter(account_id=account_id)
            transaction_list = [{'date': t.date, 'amount': t.amount, 'description': t.description} for t in transactions]
            return JsonResponse({'status': 'success', 'transactions': transaction_list})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
```