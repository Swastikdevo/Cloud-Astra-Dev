```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages

@login_required
def manage_account(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited {amount} to {account}.')
                return redirect('manage_account')

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrew {amount} from {account}.')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account')

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                amount = form.cleaned_data['amount']
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, f'Transferred {amount} from {from_account} to {to_account}.')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    context = {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }

    return render(request, 'bank/manage_account.html', context)
```