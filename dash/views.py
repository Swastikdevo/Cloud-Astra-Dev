```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages

@login_required
def account_view(request):
    account = Account.objects.get(user=request.user)
    
    # Handle deposit
    if request.method == 'POST' and 'deposit' in request.POST:
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            transaction = Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='Deposit'
            )
            messages.success(request, f'Deposit successful! New balance: {account.balance}')
            return redirect('account_view')
    else:
        deposit_form = DepositForm()

    # Handle withdrawal
    if request.method == 'POST' and 'withdraw' in request.POST:
        withdrawal_form = WithdrawalForm(request.POST)
        if withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                transaction = Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Withdrawal'
                )
                messages.success(request, f'Withdrawal successful! New balance: {account.balance}')
                return redirect('account_view')
            else:
                messages.error(request, 'Insufficient funds for this withdrawal.')
    else:
        withdrawal_form = WithdrawalForm()

    # Handle transfer
    if request.method == 'POST' and 'transfer' in request.POST:
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            recipient_username = transfer_form.cleaned_data['recipient_username']
            amount = transfer_form.cleaned_data['amount']

            try:
                recipient_account = Account.objects.get(user__username=recipient_username)
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()

                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')

                    messages.success(request, f'Transfer successful! New balance: {account.balance}')
                    return redirect('account_view')
                else:
                    messages.error(request, 'Insufficient funds for this transfer.')
            except Account.DoesNotExist:
                messages.error(request, 'Recipient account does not exist.')
    else:
        transfer_form = TransferForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/account_view.html', context)
```