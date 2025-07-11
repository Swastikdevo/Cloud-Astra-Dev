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
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        if action == 'create':
            form = AccountForm(data)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'message': 'Account created successfully!'}, status=201)
            else:
                return JsonResponse({'errors': form.errors}, status=400)

        elif action == 'delete':
            account_id = data.get('account_id')
            try:
                account = Account.objects.get(id=account_id, user=request.user)
                account.delete()
                return JsonResponse({'message': 'Account deleted successfully!'}, status=200)
            except Account.DoesNotExist:
                return JsonResponse({'error': 'Account not found.'}, status=404)

@login_required
@csrf_exempt
def record_transaction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        form = TransactionForm(data)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'message': 'Transaction recorded successfully!'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)
```