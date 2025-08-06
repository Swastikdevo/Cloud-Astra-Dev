```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages

@login_required
def manage_account(request):
    user = request.user
    account = Account.objects.filter(owner=user).first()

    if request.method == 'POST':
        # Handle deposits
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)
        transfer_form = TransferForm(request.POST)

        if 'deposit' in request.POST and deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, f'Deposited ${amount:.2f} successfully!')

        elif 'withdraw' in request.POST and withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            if amount > account.balance:
                messages.error(request, 'Insufficient balance for this withdrawal.')
            else:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                messages.success(request, f'Withdrew ${amount:.2f} successfully!')

        elif 'transfer' in request.POST and transfer_form.is_valid():
            recipient_username = transfer_form.cleaned_data['recipient']
            amount = transfer_form.cleaned_data['amount']
            recipient_account = Account.objects.filter(owner__username=recipient_username).first()

            if not recipient_account:
                messages.error(request, 'Recipient account does not exist.')
            elif amount > account.balance:
                messages.error(request, 'Insufficient balance for this transfer.')
            else:
                account.balance -= amount
                recipient_account.balance += amount
                account.save()
                recipient_account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='transfer')
                Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer')
                messages.success(request, f'Transferred ${amount:.2f} to {recipient_username} successfully!')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')

    return render(request, 'manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    })
```