```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def manage_account(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        withdraw_form = WithdrawForm(request.POST)
        transfer_form = TransferForm(request.POST)

        if 'deposit' in request.POST and deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'Deposited ${amount:.2f} successfully!')

        elif 'withdraw' in request.POST and withdraw_form.is_valid():
            amount = withdraw_form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                messages.success(request, f'Withdrew ${amount:.2f} successfully!')
            else:
                messages.error(request, 'Insufficient funds for withdrawal!')

        elif 'transfer' in request.POST and transfer_form.is_valid():
            recipient_username = transfer_form.cleaned_data['recipient']
            transfer_amount = transfer_form.cleaned_data['amount']
            try:
                recipient_account = Account.objects.get(user__username=recipient_username)
                if account.balance >= transfer_amount:
                    account.balance -= transfer_amount
                    recipient_account.balance += transfer_amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=transfer_amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=transfer_amount, transaction_type='Transfer In')
                    messages.success(request, f'Transferred ${transfer_amount:.2f} to {recipient_username} successfully!')
                else:
                    messages.error(request, 'Insufficient funds for transfer!')
            except Account.DoesNotExist:
                messages.error(request, 'Recipient account does not exist!')

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/manage_account.html', context)
```