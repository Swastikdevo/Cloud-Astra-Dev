```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': user_accounts})

@login_required
@require_POST
def deposit_funds(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'message': 'Invalid form data'})

@login_required
@require_POST
def withdraw_funds(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'message': 'Invalid form data'})

@login_required
@require_POST
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        from_account = form.cleaned_data['from_account']
        to_account = form.cleaned_data['to_account']
        amount = form.cleaned_data['amount']
        if from_account.balance >= amount:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
            return JsonResponse({'status': 'success', 'new_from_balance': from_account.balance, 'new_to_balance': to_account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'message': 'Invalid form data'})
```