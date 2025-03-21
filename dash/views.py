```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def deposit(request, account_id):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = Account.objects.get(id=account_id, user=request.user)
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'message': 'Invalid deposit amount'})

@login_required
@require_POST
def withdraw(request, account_id):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        account = Account.objects.get(id=account_id, user=request.user)
        amount = form.cleaned_data['amount']
        if amount > account.balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'message': 'Invalid withdrawal amount'})

@login_required
@require_POST
def transfer(request, account_id):
    form = TransferForm(request.POST)
    if form.is_valid():
        from_account = Account.objects.get(id=account_id, user=request.user)
        to_account = Account.objects.get(id=form.cleaned_data['to_account_id'])
        amount = form.cleaned_data['amount']
        if amount > from_account.balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()
        Transaction.objects.create(account=from_account, amount=-amount, transaction_type='Transfer Out')
        Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
        return JsonResponse({'status': 'success', 'new_balance': from_account.balance})
    return JsonResponse({'status': 'error', 'message': 'Invalid transfer details'})
```