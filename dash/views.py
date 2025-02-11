```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_GET
def account_summary(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_summary.html', {'accounts': user_accounts})

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.owner = request.user
        account.save()
        return JsonResponse({'status': 'success', 'account_id': account.id})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_POST
def make_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = Account.objects.get(id=request.POST['account_id'], owner=request.user)
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_GET
def transaction_history(request, account_id):
    transactions = Transaction.objects.filter(account_id=account_id)
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```