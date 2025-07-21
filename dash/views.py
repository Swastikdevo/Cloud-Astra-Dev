```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdrawal_form': WithdrawalForm(),
    }
    return render(request, 'bank/account_overview.html', context)

@login_required
@require_POST
def deposit_funds(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'status': 'success', 'balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_POST
def withdraw_funds(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return JsonResponse({'status': 'success', 'balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
    return JsonResponse({'status': 'error', 'errors': form.errors})
```