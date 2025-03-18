```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction

@login_required
def account_overview(request):
    """Render account overview with account details and transaction history."""
    user_accounts = Account.objects.filter(owner=request.user)
    context = {
        'accounts': user_accounts,
    }
    return render(request, 'bank/account_overview.html', context)

@login_required
@require_POST
def create_account(request):
    """Create a new bank account for the logged-in user."""
    account_name = request.POST.get('account_name')
    account_type = request.POST.get('account_type')
    
    if account_name and account_type:
        new_account = Account.objects.create(
            owner=request.user,
            name=account_name,
            account_type=account_type
        )
        return JsonResponse({'status': 'success', 'account_id': new_account.id})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid account details'})

@login_required
@require_POST
def make_transaction(request):
    """Process a transaction for a specified account."""
    account_id = request.POST.get('account_id')
    amount = request.POST.get('amount')
    transaction_type = request.POST.get('transaction_type')  # 'deposit' or 'withdraw'
    
    account = Account.objects.filter(id=account_id, owner=request.user).first()
    
    if account and amount.isdigit():
        amount = float(amount)
        if transaction_type == 'deposit':
            account.balance += amount
        elif transaction_type == 'withdraw' and account.balance >= amount:
            account.balance -= amount
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    
    return JsonResponse({'status': 'error', 'message': 'Transaction failed'})
```