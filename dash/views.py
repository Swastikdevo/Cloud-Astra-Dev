```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_dashboard(request):
    """View for the user's account dashboard."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
    }
    return render(request, 'bank_management/account_dashboard.html', context)

@require_POST
@login_required
def deposit(request):
    """View to handle deposit transactions."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()

        # Log the transaction
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        
        return JsonResponse({'status': 'success', 'new_balance': account.balance})

    return JsonResponse({'status': 'error', 'message': form.errors})

@require_POST
@login_required
def withdraw(request):
    """View to handle withdrawal transactions."""
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            # Log the transaction
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    return JsonResponse({'status': 'error', 'message': form.errors})
```