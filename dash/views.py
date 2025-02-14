```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
import json

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account_management.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create_account':
            account = Account.objects.create(
                user=request.user, 
                account_type=data.get('account_type'), 
                balance=data.get('initial_balance')
            )
            return JsonResponse({'status': 'success', 'account_id': account.id})

        elif action == 'make_transaction':
            form = TransactionForm(data)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})

        elif action == 'view_transactions':
            account_id = data.get('account_id')
            transactions = Transaction.objects.filter(account__id=account_id, user=request.user)
            transaction_data = [{'id': t.id, 'amount': t.amount, 'date': t.date} for t in transactions]
            return JsonResponse({'status': 'success', 'transactions': transaction_data})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
```