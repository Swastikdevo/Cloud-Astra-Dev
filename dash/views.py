```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def account_management(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = request.user.account
                receiver_account = form.cleaned_data['receiver_account']
                amount = form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    Transaction.objects.create(
                        account=sender_account,
                        amount=-amount,
                        transaction_type='Transfer',
                        description=f'Transferred {amount} to {receiver_account.account_number}'
                    )
                    Transaction.objects.create(
                        account=receiver_account,
                        amount=amount,
                        transaction_type='Transfer',
                        description=f'Received {amount} from {sender_account.account_number}'
                    )
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    messages.success(request, 'Transfer successful.')
                else:
                    messages.error(request, 'Insufficient funds.')
        
        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = request.user.account
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Deposit',
                    description=f'Deposited {amount}'
                )
                messages.success(request, 'Deposit successful.')
        
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = request.user.account
                amount = form.cleaned_data['amount']
                
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        amount=-amount,
                        transaction_type='Withdraw',
                        description=f'Withdrew {amount}'
                    )
                    messages.success(request, 'Withdrawal successful.')
                else:
                    messages.error(request, 'Insufficient funds.')
        return redirect('account_management')

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transactions = Transaction.objects.filter(account=request.user.account).order_by('-date')

    context = {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    }
    return render(request, 'account_management.html', context)
```