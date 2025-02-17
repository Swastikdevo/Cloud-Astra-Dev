```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

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
    return JsonResponse({'status': 'error', 'error': form.errors})

@login_required
@require_POST
def withdraw(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        return JsonResponse({'status': 'error', 'error': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'error': form.errors})

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        recipient_username = form.cleaned_data['recipient']
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)

        if account.balance >= amount:
            recipient_account = Account.objects.get(user__username=recipient_username)
            account.balance -= amount
            recipient_account.balance += amount
            account.save()
            recipient_account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        
        return JsonResponse({'status': 'error', 'error': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'error': form.errors})
```