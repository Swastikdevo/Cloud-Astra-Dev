```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    balance = sum(account.balance for account in accounts)
    return render(request, 'bank/account_overview.html', {
        'accounts': accounts,
        'total_balance': balance,
    })

@login_required
@require_POST
def deposit(request, account_id):
    account = Account.objects.get(pk=account_id, owner=request.user)
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'message': form.errors})

@login_required
@require_POST
def withdraw(request, account_id):
    account = Account.objects.get(pk=account_id, owner=request.user)
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount > account.balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'message': form.errors})
```