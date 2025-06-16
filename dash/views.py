```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': user_accounts})

@login_required
@require_POST
def deposit(request, account_id):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=account_id, owner=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def withdraw(request, account_id):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=account_id, owner=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
            return JsonResponse({'success': True, 'new_balance': account.balance})
        else:
            return JsonResponse({'success': False, 'error': 'Insufficient funds'})
    return JsonResponse({'success': False, 'errors': form.errors})
```