```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(owner=request.user)
        return render(request, 'accounts/manage.html', {'accounts': accounts})
    
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return JsonResponse({'status': 'success', 'account_id': account.id})
        return JsonResponse({'status': 'error', 'errors': form.errors})

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def account_summary(request, account_id):
    try:
        account = Account.objects.get(id=account_id, owner=request.user)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'accounts/summary.html', {'account': account, 'transactions': transactions})
    except Account.DoesNotExist:
        return redirect('accounts:manage_account')
```