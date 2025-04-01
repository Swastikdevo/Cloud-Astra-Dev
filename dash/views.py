```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'Deposited ${amount}. New balance: ${account.balance}')
                return redirect('account_overview')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    messages.success(request, f'Withdrew ${amount}. New balance: ${account.balance}')
                    return redirect('account_overview')
                else:
                    messages.error(request, 'Insufficient funds!')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_username = transfer_form.cleaned_data['recipient']
                amount = transfer_form.cleaned_data['amount']
                recipient = Account.objects.filter(user__username=recipient_username).first()

                if recipient and account.balance >= amount:
                    account.balance -= amount
                    recipient.balance += amount
                    account.save()
                    recipient.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=recipient, amount=amount, transaction_type='transfer_in')
                    messages.success(request, f'Transferred ${amount} to {recipient_username}.')
                    return redirect('account_overview')
                elif not recipient:
                    messages.error(request, 'Recipient not found!')
                else:
                    messages.error(request, 'Insufficient funds!')

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
    
    return render(request, 'account_overview.html', context)
```