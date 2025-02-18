```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def account_overview(request):
    """Display the user's account overview including balance and recent transactions."""
    user_accounts = Account.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')[:5]
    total_balance = sum(account.balance for account in user_accounts)
    
    context = {
        'accounts': user_accounts,
        'transactions': transactions,
        'total_balance': total_balance,
    }
    return render(request, 'bank/account_overview.html', context)

@login_required
@require_POST
def deposit(request, account_id):
    """Handle deposit transactions for a user's account."""
    account = Account.objects.get(id=account_id, owner=request.user)
    form = TransactionForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        account.balance += amount
        account.save()
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_POST
def withdraw(request, account_id):
    """Handle withdrawal transactions from a user's account."""
    account = Account.objects.get(id=account_id, owner=request.user)
    form = TransactionForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount <= account.balance:
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            account.balance -= amount
            account.save()
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def transaction_history(request):
    """Display a user's transaction history."""
    user_accounts = Account.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')
    
    context = {
        'transactions': transactions,
    }
    return render(request, 'bank/transaction_history.html', context)
```