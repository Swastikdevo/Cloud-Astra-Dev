```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from django.db import transaction
from datetime import datetime

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def deposit_funds(request, account_id):
    amount = float(request.POST.get('amount', 0))
    account = Account.objects.get(id=account_id, user=request.user)

    with transaction.atomic():
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit', date=datetime.now())

    return JsonResponse({'success': True, 'new_balance': account.balance})

@login_required
@require_POST
def withdraw_funds(request, account_id):
    amount = float(request.POST.get('amount', 0))
    account = Account.objects.get(id=account_id, user=request.user)

    if account.balance >= amount:
        with transaction.atomic():
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal', date=datetime.now())
        return JsonResponse({'success': True, 'new_balance': account.balance})
    else:
        return JsonResponse({'success': False, 'error': 'Insufficient funds'}, status=400)

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})
```