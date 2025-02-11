```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_dashboard(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                account.balance += amount
                account.save()
                messages.success(request, 'Deposit successful!')
                return redirect('account_dashboard')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                account = withdrawal_form.cleaned_data['account']
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    account.balance -= amount
                    account.save()
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('account_dashboard')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                source_account = transfer_form.cleaned_data['source_account']
                target_account = transfer_form.cleaned_data['target_account']
                amount = transfer_form.cleaned_data['amount']
                if source_account.balance >= amount:
                    Transaction.objects.create(account=source_account, amount=-amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds for transfer!')
                return redirect('account_dashboard')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    context = {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form
    }
    return render(request, 'bank/account_dashboard.html', context)
```