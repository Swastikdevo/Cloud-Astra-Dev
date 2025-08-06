```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save()
        return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@csrf_exempt
@require_POST
def make_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save()
        account = get_object_or_404(Account, id=transaction.account.id)
        account.balance += transaction.amount if transaction.type == 'credit' else -transaction.amount
        account.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=201)
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'account/details.html', {'account': account, 'transactions': transactions})

def list_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'account/list.html', {'accounts': accounts})

def account_balance(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    return JsonResponse({'account_id': account.id, 'balance': account.balance})
```