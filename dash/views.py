```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_GET
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_list.html', {'accounts': accounts})

@login_required
@require_GET
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        new_account = form.save(commit=False)
        new_account.user = request.user
        new_account.save()
        return JsonResponse({'success': True, 'account_id': new_account.id})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()
        return JsonResponse({'success': True, 'transaction_id': transaction.id})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_GET
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})
```