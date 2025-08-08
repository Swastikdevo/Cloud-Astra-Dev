```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, WithdrawForm, DepositForm

@login_required
def bank_account_view(request):
    account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Handle fund transfer
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                receiver_account = transfer_form.cleaned_data['receiver_account']
                amount = transfer_form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(
                        sender=account,
                        receiver=receiver_account,
                        amount=amount,
                        transaction_type='Transfer'
                    )
                    account.balance -= amount
                    receiver_account.balance += amount
                    account.save()
                    receiver_account.save()
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient balance!')
                return redirect('bank_account')

        # Handle withdrawal
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(
                        sender=account,
                        amount=amount,
                        transaction_type='Withdrawal'
                    )
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient balance!')
                return redirect('bank_account')
        
        # Handle deposit
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    receiver=account,
                    amount=amount,
                    transaction_type='Deposit'
                )
                messages.success(request, 'Deposit successful!')
                return redirect('bank_account')

    transfer_form = TransferForm()
    withdraw_form = WithdrawForm()
    deposit_form = DepositForm()
    
    context = {
        'account': account,
        'transfer_form': transfer_form,
        'withdraw_form': withdraw_form,
        'deposit_form': deposit_form,
    }
    
    return render(request, 'bank/account.html', context)
```