```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_dashboard(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    return render(request, 'account/dashboard.html', {
        'account': user_account,
        'transactions': transactions,
    })

@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_account = Account.objects.get(user=request.user)
            user_account.balance += amount
            user_account.save()
            Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'Deposit of ${amount} successful!')
            return redirect('account_dashboard')
    else:
        form = DepositForm()
    
    return render(request, 'account/deposit.html', {'form': form})

@login_required
def withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_account = Account.objects.get(user=request.user)
            if user_account.balance >= amount:
                user_account.balance -= amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdraw')
                messages.success(request, f'Withdrawal of ${amount} successful!')
            else:
                messages.error(request, 'Insufficient funds!')
            return redirect('account_dashboard')
    else:
        form = WithdrawForm()
    
    return render(request, 'account/withdraw.html', {'form': form})

@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient_username']
            amount = form.cleaned_data['amount']
            user_account = Account.objects.get(user=request.user)

            try:
                recipient_account = Account.objects.get(user__username=recipient_username)
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Transfer to ' + recipient_username)
                    messages.success(request, f'Transfer of ${amount} to {recipient_username} successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
            except Account.DoesNotExist:
                messages.error(request, 'Recipient does not exist!')

            return redirect('account_dashboard')
    else:
        form = TransferForm()
    
    return render(request, 'account/transfer.html', {'form': form})
```