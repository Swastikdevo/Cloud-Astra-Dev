```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == 'GET':
        if account_id:
            account = Account.objects.get(id=account_id)
            return render(request, 'account_detail.html', {'account': account})
        else:
            accounts = Account.objects.all()
            return render(request, 'account_list.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            if account_id:
                account = Account.objects.get(id=account_id)
                for attr, value in form.cleaned_data.items():
                    setattr(account, attr, value)
                account.save()
            else:
                account = form.save()
            return JsonResponse({'status': 'success', 'account_id': account.id})

    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def perform_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def account_balance(request, account_id):
    if request.method == 'GET':
        account = Account.objects.get(id=account_id)
        balance = account.balance
        return JsonResponse({'account_id': account_id, 'balance': balance})

    return JsonResponse({'status': 'error'}, status=400)
```