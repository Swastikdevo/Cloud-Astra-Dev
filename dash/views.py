```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_account = transfer_form.cleaned_data['recipient']
                amount = transfer_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    Transaction.objects.create(
                        sender=user_account,
                        recipient=recipient_account,
                        amount=amount,
                        transaction_type='Transfer'
                    )
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    messages.success(request, 'Transfer Successful!')
                else:
                    messages.error(request, 'Insufficient Funds!')
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(
                    account=user_account,
                    amount=amount,
                    transaction_type='Deposit'
                )
                messages.success(request, 'Deposit Successful!')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(
                        account=user_account,
                        amount=amount,
                        transaction_type='Withdrawal'
                    )
                    messages.success(request, 'Withdrawal Successful!')
                else:
                    messages.error(request, 'Insufficient Funds!')

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transactions = Transaction.objects.filter(account=user_account)

    context = {
        'user_account': user_account,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    }
    return render(request, 'bank/manage_account.html', context)
```