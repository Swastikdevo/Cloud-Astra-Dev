```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_dashboard(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('account_dashboard')

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawalForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('account_dashboard')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                target_account = transfer_form.cleaned_data['target_account']
                amount = transfer_form.cleaned_data['amount']
                if account.balance >= amount:
                    target_account.balance += amount
                    target_account.save()
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer', target_account=target_account)
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds for transfer!')
                return redirect('account_dashboard')

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawalForm()
        transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'account/dashboard.html', context)
```