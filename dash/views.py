```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        withdraw_form = WithdrawForm(request.POST)
        transfer_form = TransferForm(request.POST)

        if 'deposit' in request.POST and deposit_form.is_valid():
            account = deposit_form.cleaned_data['account']
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'${amount} deposited to your account.')

        elif 'withdraw' in request.POST and withdraw_form.is_valid():
            account = withdraw_form.cleaned_data['account']
            amount = withdraw_form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                messages.success(request, f'${amount} withdrawn from your account.')
            else:
                messages.error(request, 'Insufficient funds.')

        elif 'transfer' in request.POST and transfer_form.is_valid():
            source_account = transfer_form.cleaned_data['source_account']
            target_account = transfer_form.cleaned_data['target_account']
            amount = transfer_form.cleaned_data['amount']
            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                Transaction.objects.create(account=source_account, amount=amount, transaction_type='Transfer')
                messages.success(request, f'${amount} transferred from {source_account} to {target_account}.')
            else:
                messages.error(request, 'Insufficient funds to transfer.')

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
    
    return render(request, 'bank/account_dashboard.html', context)
```