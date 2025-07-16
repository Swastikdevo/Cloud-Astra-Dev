```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_management_view(request):
    user_accounts = Account.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount} successfully!')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    messages.success(request, f'Withdrew ${amount} successfully!')
                else:
                    messages.error(request, 'Insufficient balance.')
                return redirect('bank_management')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, f'Transferred ${amount} successfully!')
                else:
                    messages.error(request, 'Insufficient balance for transfer.')
                return redirect('bank_management')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    return render(request, 'bank_management.html', {
        'user_accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    })
```