```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def account_overview(request):
    """Displays the account overview including balance and recent transactions."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    return render(request, 'account/overview.html', {
        'account': account,
        'transactions': transactions
    })

@login_required
@require_POST
def deposit(request):
    """Handles deposit requests."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        messages.success(request, f'Deposited ${amount:.2f} successfully.')
        return redirect('account_overview')
    messages.error(request, 'Invalid deposit amount.')
    return redirect('account_overview')

@login_required
@require_POST
def withdraw(request):
    """Handles withdrawal requests."""
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            messages.success(request, f'Withdrew ${amount:.2f} successfully.')
        else:
            messages.error(request, 'Insufficient funds for this withdrawal.')
    else:
        messages.error(request, 'Invalid withdrawal amount.')
    return redirect('account_overview')

@login_required
def transaction_history(request):
    """Displays the transaction history."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'account/transaction_history.html', {
        'transactions': transactions
    })
```