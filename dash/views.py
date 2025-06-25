```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

@login_required
def account_dashboard(request):
    """Render the user's account dashboard with balance and transaction history."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
        'transfer_form': TransferForm(),
    }
    return render(request, 'bank/account_dashboard.html', context)

@require_POST
@login_required
def deposit(request):
    """Handle the deposit functionality."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()

        Transaction.objects.create(account=account, amount=amount, type='Deposit')
        messages.success(request, 'Deposit successful!')
        return redirect('account_dashboard')
    else:
        messages.error(request, 'Invalid deposit amount!')
        return redirect('account_dashboard')

@require_POST
@login_required
def withdraw(request):
    """Handle the withdrawal functionality."""
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, type='Withdrawal')
            messages.success(request, 'Withdrawal successful!')
        else:
            messages.error(request, 'Insufficient funds!')
    else:
        messages.error(request, 'Invalid withdrawal amount!')
    
    return redirect('account_dashboard')

@require_POST
@login_required
def transfer(request):
    """Handle the fund transfer functionality."""
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        recipient_username = form.cleaned_data['recipient']
        account = Account.objects.get(user=request.user)
        
        if amount <= account.balance:
            recipient = Account.objects.get(user__username=recipient_username)
            account.balance -= amount
            recipient.balance += amount
            account.save()
            recipient.save()
            Transaction.objects.create(account=account, amount=amount, type='Transfer', recipient=recipient)
            messages.success(request, 'Transfer successful!')
        else:
            messages.error(request, 'Insufficient funds!')
    else:
        messages.error(request, 'Invalid transfer details!')
    
    return redirect('account_dashboard')
```