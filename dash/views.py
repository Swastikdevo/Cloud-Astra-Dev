```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts)
        return render(request, 'bank_management.html', {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm()
        })

    elif request.method == 'POST':
        data = json.loads(request.body)
        
        if data.get('action') == 'create_account':
            form = AccountForm(data)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'account_id': account.id})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        elif data.get('action') == 'create_transaction':
            form = TransactionForm(data)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = Account.objects.get(id=data['account_id'], user=request.user)
                transaction.save()
                return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        elif data.get('action') == 'delete_account':
            account = Account.objects.get(id=data['account_id'], user=request.user)
            account.delete()
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
```