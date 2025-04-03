```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    """Display the account overview with balance and recent transactions."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/account_overview.html', context)

@login_required
@require_POST
def deposit(request):
    """Deposit money into the user's account."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()

        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'success': True, 'balance': account.balance})

    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def withdraw(request):
    """Withdraw money from the user's account."""
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)

        if amount > account.balance:
            return JsonResponse({'success': False, 'errors': 'Insufficient funds'})
        
        account.balance -= amount
        account.save()
        
        Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
        return JsonResponse({'success': True, 'balance': account.balance})

    return JsonResponse({'success': False, 'errors': form.errors})
```