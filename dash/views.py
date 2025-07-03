```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.contrib.auth.decorators import login_required

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'account/dashboard.html', {'accounts': user_accounts})

@csrf_exempt
@require_POST
@login_required
def deposit_funds(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        if amount > 0 and account.owner == request.user:
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return JsonResponse({'status': 'success', 'balance': account.balance})
    return JsonResponse({'status': 'error', 'message': 'Invalid deposit request'})

@csrf_exempt
@require_POST
@login_required
def withdraw_funds(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        if amount > 0 and account.owner == request.user and account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
            return JsonResponse({'status': 'success', 'balance': account.balance})
    return JsonResponse({'status': 'error', 'message': 'Invalid withdrawal request'})

@login_required
def transaction_history(request):
    user_accounts = Account.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')
    return render(request, 'account/transactions.html', {'transactions': transactions})
```