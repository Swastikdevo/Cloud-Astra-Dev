```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': user_accounts})

@login_required
def deposit_funds(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'Deposited ${amount} to your account.')
            return redirect('account_overview')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit_funds.html', {'form': form, 'account': account})

@login_required
def withdraw_funds(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                messages.success(request, f'Withdrew ${amount} from your account.')
                return redirect('account_overview')
            else:
                messages.error(request, 'Insufficient balance.')
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw_funds.html', {'form': form, 'account': account})

@login_required
def transfer_funds(request, account_id):
    sender_account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            try:
                recipient_account = Account.objects.get(owner__username=recipient_username)
                if amount <= sender_account.balance:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, f'Transferred ${amount} to {recipient_username}.')
                    return redirect('account_overview')
                else:
                    messages.error(request, 'Insufficient balance.')
            except Account.DoesNotExist:
                messages.error(request, 'Recipient account does not exist.')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer_funds.html', {'form': form, 'account': sender_account})
```