```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        return render(request, 'bank/accounts.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        form = AccountForm(data)

        if form.is_valid():
            account = form.save()
            return JsonResponse({'id': account.id, 'message': 'Account created successfully!'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def make_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = TransactionForm(data)

        if form.is_valid():
            transaction = form.save()
            account = transaction.account
            return JsonResponse({'id': transaction.id, 'balance': account.balance, 'message': 'Transaction successful!'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
```