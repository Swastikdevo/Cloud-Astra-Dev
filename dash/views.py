```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@require_GET
def account_overview(request):
    """Display account details and recent transactions."""
    user_account = Account.objects.get(user=request.user)
    recent_transactions = Transaction.objects.filter(account=user_account).order_by('-date')[:5]
    return render(request, 'bank/account_overview.html', {
        'account': user_account,
        'transactions': recent_transactions,
    })

@login_required
@require_POST
def deposit_funds(request):
    """Handle deposits to the user's account."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        user_account = Account.objects.get(user=request.user)
        user_account.balance += amount
        user_account.save()
        Transaction.objects.create(account=user_account, amount=amount, transaction_type='deposit')
        return redirect('account_overview')
    return render(request, 'bank/deposit.html', {'form': form})

@login_required
@require_POST
def withdraw_funds(request):
    """Handle withdrawals from the user's account."""
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        user_account = Account.objects.get(user=request.user)
        if user_account.balance >= amount:
            user_account.balance -= amount
            user_account.save()
            Transaction.objects.create(account=user_account, amount=amount, transaction_type='withdrawal')
            return redirect('account_overview')
        else:
            form.add_error(None, 'Insufficient funds.')
    return render(request, 'bank/withdraw.html', {'form': form})
```