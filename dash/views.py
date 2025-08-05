```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_GET
def account_dashboard(request):
    """Display the account dashboard with account details and transactions."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_dashboard.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
def deposit(request):
    """Handle deposit requests and update account balance."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        messages.success(request, 'Deposit successful.')
        return redirect('account_dashboard')
    messages.error(request, 'Invalid deposit amount.')
    return redirect('account_dashboard')

@login_required
@require_POST
def withdraw(request):
    """Handle withdrawal requests and update account balance."""
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            messages.success(request, 'Withdrawal successful.')
        else:
            messages.error(request, 'Insufficient funds.')
    else:
        messages.error(request, 'Invalid withdrawal amount.')
    return redirect('account_dashboard')

@login_required
@require_POST
def transfer(request):
    """Handle fund transfer between accounts."""
    form = TransferForm(request.POST)
    if form.is_valid():
        target_account_id = form.cleaned_data['target_account']
        amount = form.cleaned_data['amount']
        source_account = Account.objects.get(user=request.user)
        target_account = Account.objects.get(id=target_account_id)

        if amount <= source_account.balance:
            source_account.balance -= amount
            target_account.balance += amount
            source_account.save()
            target_account.save()
            Transaction.objects.create(account=source_account, amount=amount, transaction_type='Transfer Out', target_account=target_account)
            Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In', source_account=source_account)
            messages.success(request, 'Transfer successful.')
        else:
            messages.error(request, 'Insufficient funds for transfer.')
    else:
        messages.error(request, 'Invalid transfer details.')
    return redirect('account_dashboard')
```