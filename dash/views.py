```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)
        
        if form.is_valid():
            account = form.save()
            return JsonResponse({'status': 'success', 'account_id': account.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        account = Account.objects.get(id=account_id) if account_id else None
        form = AccountForm(instance=account)
        return render(request, 'account_form.html', {'form': form})

@csrf_exempt
def make_transaction(request, account_id):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=account_id)
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return render(request, 'transaction_form.html', {'account_id': account_id})

def account_details(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'account_details.html', {'account': account, 'transactions': transactions})
```