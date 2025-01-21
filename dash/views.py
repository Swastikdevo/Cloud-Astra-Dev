```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.db import transaction
from django.views.decorators.http import require_POST

@login_required
def account_overview(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    return render(request, 'accounts/overview.html', {'accounts': accounts})

@login_required
@require_POST
def deposit_funds(request, account_id):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=account_id, owner=request.user)
        with transaction.atomic():
            account.balance += amount
            account.save()
            transaction_record = Transaction(account=account, amount=amount, transaction_type='Deposit')
            transaction_record.save()
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_POST
def withdraw_funds(request, account_id):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=account_id, owner=request.user)
        if account.balance >= amount:
            with transaction.atomic():
                account.balance -= amount
                account.save()
                transaction_record = Transaction(account=account, amount=amount, transaction_type='Withdrawal')
                transaction_record.save()
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'errors': form.errors})
```