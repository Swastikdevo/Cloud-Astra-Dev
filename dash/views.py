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
            return JsonResponse({'status': 'success', 'account_id': account.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    accounts = Account.objects.all()
    return render(request, 'manage_account.html', {'accounts': accounts})

@csrf_exempt
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    return render(request, 'make_transaction.html', {'form': TransactionForm()})

def view_account_details(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'account_details.html', {'account': account, 'transactions': transactions})
```