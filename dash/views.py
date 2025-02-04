```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)
    else:
        accounts = Account.objects.all()
    
    return render(request, 'bank/manage_account.html', {'accounts': accounts, 'form': AccountForm()})

@csrf_exempt
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=201)
    return render(request, 'bank/create_transaction.html', {'form': TransactionForm()})

def view_account_balance(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        balance = account.balance
        return JsonResponse({'status': 'success', 'balance': balance})
    except Account.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)

def view_transactions(request, account_id):
    try:
        transactions = Transaction.objects.filter(account__id=account_id).values()
        return JsonResponse({'status': 'success', 'transactions': list(transactions)})
    except Account.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)
```