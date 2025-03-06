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
        transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
        context = {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm(),
        }
        return render(request, 'bank_management.html', context)

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create_account':
            form = AccountForm(data)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return JsonResponse({'status': 'success', 'account_id': new_account.id}, status=201)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        elif action == 'create_transaction':
            form = TransactionForm(data)
            if form.is_valid():
                new_transaction = form.save(commit=False)
                new_transaction.account = Account.objects.get(id=data.get('account_id'))
                new_transaction.save()
                return JsonResponse({'status': 'success', 'transaction_id': new_transaction.id}, status=201)
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
```