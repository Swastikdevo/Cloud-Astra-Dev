```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount} successfully!')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrew ${amount} successfully!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                transfer_amount = transfer_form.cleaned_data['amount']
                recipient_username = transfer_form.cleaned_data['recipient']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    if transfer_amount <= account.balance:
                        account.balance -= transfer_amount
                        recipient_account.balance += transfer_amount
                        account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=account, amount=-transfer_amount, transaction_type='Transfer Out')
                        Transaction.objects.create(account=recipient_account, amount=transfer_amount, transaction_type='Transfer In')
                        messages.success(request, f'Transferred ${transfer_amount} to {recipient_username} successfully!')
                    else:
                        messages.error(request, 'Insufficient funds for transfer!')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist!')
                return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    return render(request, 'bank/manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })
```