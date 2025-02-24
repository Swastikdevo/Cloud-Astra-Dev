```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_dashboard(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)
        transfer_form = TransferForm(request.POST)

        if deposit_form.is_valid():
            account = deposit_form.cleaned_data['account']
            amount = deposit_form.cleaned_data['amount']
            transaction = Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            account.balance += amount
            account.save()
            messages.success(request, f'Deposited ${amount} to {account.name}')
            return redirect('bank_dashboard')

        elif withdrawal_form.is_valid():
            account = withdrawal_form.cleaned_data['account']
            amount = withdrawal_form.cleaned_data['amount']
            if account.balance >= amount:
                transaction = Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                account.balance -= amount
                account.save()
                messages.success(request, f'Withdrew ${amount} from {account.name}')
                return redirect('bank_dashboard')
            else:
                messages.error(request, 'Insufficient funds')

        elif transfer_form.is_valid():
            from_account = transfer_form.cleaned_data['from_account']
            to_account = transfer_form.cleaned_data['to_account']
            amount = transfer_form.cleaned_data['amount']
            if from_account.balance >= amount:
                transaction_out = Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                transaction_in = Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                messages.success(request, f'Transferred ${amount} from {from_account.name} to {to_account.name}')
                return redirect('bank_dashboard')
            else:
                messages.error(request, 'Insufficient funds for transfer')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    context = {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/dashboard.html', context)
```