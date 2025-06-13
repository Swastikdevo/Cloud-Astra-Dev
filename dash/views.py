```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def deposit(request, account_id):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=account_id, user=request.user)
        account.balance += amount
        account.save()
        transaction = Transaction(account=account, amount=amount, transaction_type='Deposit')
        transaction.save()
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_POST
def withdraw(request, account_id):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=account_id, user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            transaction = Transaction(account=account, amount=amount, transaction_type='Withdraw')
            transaction.save()
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
    return JsonResponse({'status': 'error', 'errors': form.errors})
```