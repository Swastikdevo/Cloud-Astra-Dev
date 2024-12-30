```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    return redirect('manage_account')
                else:
                    return HttpResponse("Insufficient funds.")
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_username = transfer_form.cleaned_data['recipient_username']
                amount = transfer_form.cleaned_data['amount']
                recipient_account = Account.objects.get(user__username=recipient_username)
                if amount <= account.balance:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer')
                    return redirect('manage_account')
                else:
                    return HttpResponse("Insufficient funds.")

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'manage_account.html', context)
```