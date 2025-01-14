```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def bank_management_view(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = Account.objects.get(user=request.user)
                amount = transfer_form.cleaned_data['amount']
                recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient_account_number'])

                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, transaction_type='Transfer', amount=amount)
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds for this transfer.')
                return redirect('bank_management')

        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = Account.objects.get(user=request.user)
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, transaction_type='Deposit', amount=amount)
                messages.success(request, 'Deposit successful!')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = Account.objects.get(user=request.user)
                amount = withdraw_form.cleaned_data['amount']

                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, transaction_type='Withdraw', amount=amount)
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds for this withdrawal.')
                return redirect('bank_management')

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    return render(request, 'bank_management.html', {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```