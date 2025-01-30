```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    return render(request, 'bank/account_overview.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid deposit amount'})

@login_required
@require_POST
def withdraw(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if amount > account.balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
        
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})

    return JsonResponse({'status': 'error', 'message': 'Invalid withdrawal amount'})
```