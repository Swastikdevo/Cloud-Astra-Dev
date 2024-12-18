```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_accounts(request):
    if request.method == "GET":
        accounts = Account.objects.filter(owner=request.user)
        return render(request, 'bank/manage_accounts.html', {'accounts': accounts})
    
    elif request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return JsonResponse({'status': 'success', 'account_id': account.id})
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@csrf_exempt
def make_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
```