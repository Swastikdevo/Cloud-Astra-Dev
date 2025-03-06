```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_summary')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('account_summary')
                else:
                    return HttpResponse('Insufficient funds.')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_account = transfer_form.cleaned_data['recipient']
                amount = transfer_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    recipient = Account.objects.get(account_number=recipient_account)
                    recipient.balance += amount
                    account.save()
                    recipient.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer')
                    Transaction.objects.create(account=recipient, amount=amount, transaction_type='Received Transfer')
                    return redirect('account_summary')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    context = {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'manage_account.html', context)
```