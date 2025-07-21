```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    # Handle depositing money
    if request.method == 'POST' and 'deposit' in request.POST:
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, 'Deposit successful!')
            return redirect('manage_account')

    # Handle withdrawing money
    elif request.method == 'POST' and 'withdraw' in request.POST:
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                messages.success(request, 'Withdrawal successful!')
            else:
                messages.error(request, 'Insufficient balance!')
            return redirect('manage_account')

    # Handle transferring money
    elif request.method == 'POST' and 'transfer' in request.POST:
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            sender_account = Account.objects.get(user=request.user)
            recipient_account = Account.objects.get(user__username=recipient_username)
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()
                Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='Transfer')
                Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer')
                messages.success(request, 'Transfer successful!')
            else:
                messages.error(request, 'Insufficient balance!')
            return redirect('manage_account')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()
    
    context = {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'balance': Account.objects.get(user=request.user).balance,
    }
    return render(request, 'bank/manage_account.html', context)
```