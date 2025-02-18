```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(owner=request.user)
        return render(request, 'manage_accounts.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        if 'create' in data:
            form = AccountForm(data)
            if form.is_valid():
                account = form.save(commit=False)
                account.owner = request.user
                account.save()
                return JsonResponse({'success': True, 'account_id': account.id}, status=201)
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        elif 'delete' in data:
            account_id = data['account_id']
            try:
                account = Account.objects.get(id=account_id, owner=request.user)
                account.delete()
                return JsonResponse({'success': True}, status=200)
            except Account.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Account not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Bad request'}, status=400)

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'success': True, 'transaction_id': transaction.id}, status=201)

    return JsonResponse({'success': False, 'error': 'Invalid transaction data'}, status=400)
```