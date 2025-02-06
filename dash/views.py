```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_home(request):
    """Render the account homepage with account details and recent transactions."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]
    
    return render(request, 'accounts/home.html', {
        'account': account,
        'transactions': transactions
    })

@login_required
@require_POST
def deposit(request):
    """Handle deposit transactions."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        
        Transaction.objects.create(
            account=account,
            amount=amount,
            transaction_type='deposit'
        )
        return JsonResponse({'success': True, 'new_balance': account.balance})
    
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def withdraw(request):
    """Handle withdrawal transactions."""
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)

        if account.balance >= amount:
            account.balance -= amount
            account.save()

            Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='withdrawal'
            )
            return JsonResponse({'success': True, 'new_balance': account.balance})
        else:
            return JsonResponse({'success': False, 'error': 'Insufficient funds'})

    return JsonResponse({'success': False, 'errors': form.errors})
```