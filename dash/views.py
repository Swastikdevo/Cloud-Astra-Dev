```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required

@login_required
def account_dashboard(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    balance = account.balance
    
    context = {
        'account': account,
        'transactions': transactions,
        'balance': balance,
    }
    return render(request, 'bank/account_dashboard.html', context)

@login_required
@require_POST
def deposit(request):
    amount = float(request.POST.get('amount', 0))
    account = Account.objects.get(user=request.user)
    if amount > 0:
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        return JsonResponse({'status': 'success', 'balance': account.balance})
    return JsonResponse({'status': 'error', 'message': 'Invalid amount'})

@login_required
@require_POST
def withdraw(request):
    amount = float(request.POST.get('amount', 0))
    account = Account.objects.get(user=request.user)
    if 0 < amount <= account.balance:
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
        return JsonResponse({'status': 'success', 'balance': account.balance})
    return JsonResponse({'status': 'error', 'message': 'Insufficient funds or invalid amount'})

@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'transactions': transactions,
    }
    return render(request, 'bank/transaction_history.html', context)
```