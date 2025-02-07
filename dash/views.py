```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.contrib import messages

@method_decorator(login_required, name='dispatch')
def bank_dashboard(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                account_from = transfer_form.cleaned_data['account_from']
                account_to = transfer_form.cleaned_data['account_to']
                amount = transfer_form.cleaned_data['amount']
                
                # Implement Transfer
                if account_from.balance >= amount:
                    account_from.balance -= amount
                    account_to.balance += amount
                    account_from.save()
                    account_to.save()
                    
                    Transaction.objects.create(
                        from_account=account_from,
                        to_account=account_to,
                        amount=amount,
                        transaction_type='Transfer'
                    )
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient balance for transfer.')
        
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']

                # Implement Deposit
                account.balance += amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Deposit'
                )
                messages.success(request, 'Deposit successful!')

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = withdraw_form.cleaned_data['account']
                amount = withdraw_form.cleaned_data['amount']

                # Implement Withdraw
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()

                    Transaction.objects.create(
                        account=account,
                        amount=amount,
                        transaction_type='Withdraw'
                    )
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient balance for withdrawal.')

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    accounts = Account.objects.filter(user=request.user)
    context = {
        'accounts': accounts,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'bank/dashboard.html', context)
```