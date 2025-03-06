```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_management(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        # Handle deposit
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            user_account.balance += amount
            user_account.save()
            Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'Deposit successful! Your new balance is {user_account.balance}.')
            return redirect('account_management')

        # Handle withdrawal
        withdraw_form = WithdrawForm(request.POST)
        if withdraw_form.is_valid():
            amount = withdraw_form.cleaned_data['amount']
            if amount > user_account.balance:
                messages.error(request, 'Insufficient funds for withdrawal.')
            else:
                user_account.balance -= amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Withdrawal')
                messages.success(request, f'Withdrawal successful! Your new balance is {user_account.balance}.')
                return redirect('account_management')

        # Handle transfer
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            recipient_username = transfer_form.cleaned_data['recipient']
            amount = transfer_form.cleaned_data['amount']
            if amount > user_account.balance:
                messages.error(request, 'Insufficient funds for transfer.')
            else:
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Transfer to ' + recipient_username)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from ' + request.user.username)
                    messages.success(request, f'Transfer successful! Your new balance is {user_account.balance}.')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist.')
                return redirect('account_management')

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'bank/account_management.html', context)
```