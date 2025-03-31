```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@require_GET
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
        
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        
        return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def withdraw(request, account_id):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        account = Account.objects.get(id=account_id, user=request.user)
        amount = form.cleaned_data['amount']
        
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            
            return JsonResponse({'success': True, 'new_balance': account.balance})
        return JsonResponse({'success': False, 'error': 'Insufficient funds.'})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_GET
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```