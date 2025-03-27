```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

@login_required
def bank_management_view(request):
    user_accounts = Account.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount} to {account.account_number}.')
                return redirect('bank_management')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    messages.success(request, f'Withdrew ${amount} from {account.account_number}.')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_management')
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = form.cleaned_data['sender_account']
                receiver_account = form.cleaned_data['receiver_account']
                amount = form.cleaned_data['amount']
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer to ' + receiver_account.account_number)
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='Transfer from ' + sender_account.account_number)
                    messages.success(request, f'Transferred ${amount} from {sender_account.account_number} to {receiver_account.account_number}.')
                else:
                    messages.error(request, 'Insufficient funds for the transfer.')
                return redirect('bank_management')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'user_accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }

    return render(request, 'bank_management.html', context)
```