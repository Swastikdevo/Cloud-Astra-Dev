```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@require_POST
@login_required
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@require_POST
@login_required
def withdraw(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
        if amount > account.balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@require_POST
@login_required
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        from_account = Account.objects.get(id=form.cleaned_data['from_account_id'], user=request.user)
        to_account = Account.objects.get(id=form.cleaned_data['to_account_id'])
        
        if amount > from_account.balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
        
        from_account.balance -= amount
        to_account.balance += amount
        
        from_account.save()
        to_account.save()
        
        Transaction.objects.create(account=from_account, amount=-amount, transaction_type='Transfer Out')
        Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
        
        return JsonResponse({'status': 'success', 'new_from_balance': from_account.balance, 'new_to_balance': to_account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})
```