```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                from_account = transfer_form.cleaned_data['from_account']
                to_account = transfer_form.cleaned_data['to_account']
                
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(
                        account=from_account,
                        type='Transfer Out',
                        amount=amount
                    )
                    Transaction.objects.create(
                        account=to_account,
                        type='Transfer In',
                        amount=amount
                    )
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = deposit_form.cleaned_data['account']
                
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    type='Deposit',
                    amount=amount
                )
                messages.success(request, 'Deposit successful!')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                account = withdraw_form.cleaned_data['account']
                
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        type='Withdrawal',
                        amount=amount
                    )
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
    
    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    return render(request, 'bank/dashboard.html', {
        'user_accounts': user_accounts,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```