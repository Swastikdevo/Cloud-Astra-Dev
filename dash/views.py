```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@csrf_exempt
@require_POST
@login_required
def deposit_funds(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account_id = form.cleaned_data['account']
        account = Account.objects.get(id=account_id, user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        return JsonResponse({'status': 'success', 'balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@csrf_exempt
@require_POST
@login_required
def withdraw_funds(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account_id = form.cleaned_data['account']
        account = Account.objects.get(id=account_id, user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            return JsonResponse({'status': 'success', 'balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```