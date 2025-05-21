```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_dashboard(request):
    """Display user account dashboard with balance and transaction history."""
    
    # Retrieve the current user's account
    account = get_object_or_404(Account, user=request.user)
    
    # Get user's recent transactions
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    
    return render(request, 'bank/account_dashboard.html', context)

@login_required
def deposit_view(request):
    """Handle deposit transactions."""
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = get_object_or_404(Account, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, txn_type='deposit')
            messages.success(request, f'You have successfully deposited ${amount}.')
            return redirect('account_dashboard')
    else:
        form = DepositForm()
    
    return render(request, 'bank/deposit.html', {'form': form})

@login_required
def withdraw_view(request):
    """Handle withdrawal transactions."""
    
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = get_object_or_404(Account, user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=-amount, txn_type='withdrawal')
                messages.success(request, f'You have successfully withdrawn ${amount}.')
                return redirect('account_dashboard')
            else:
                messages.error(request, 'Insufficient balance for withdrawal.')
    else:
        form = WithdrawForm()
    
    return render(request, 'bank/withdraw.html', {'form': form})

@login_required
def transfer_view(request):
    """Handle money transfers between user accounts."""
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_username = form.cleaned_data['recipient']
            sender_account = get_object_or_404(Account, user=request.user)
            recipient_account = get_object_or_404(Account, user__username=recipient_username)
            
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()
                Transaction.objects.create(account=sender_account, amount=-amount, txn_type='transfer', recipient=recipient_account)
                Transaction.objects.create(account=recipient_account, amount=amount, txn_type='transfer', sender=sender_account)
                messages.success(request, f'You have successfully transferred ${amount} to {recipient_username}.')
                return redirect('account_dashboard')
            else:
                messages.error(request, 'Insufficient balance for transfer.')
    else:
        form = TransferForm()
    
    return render(request, 'bank/transfer.html', {'form': form})
```