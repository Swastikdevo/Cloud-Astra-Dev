```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

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
                return redirect('account_overview')

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('account_overview')
                else:
                    return HttpResponse("Insufficient balance.")

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                target_username = transfer_form.cleaned_data['target_user']
                amount = transfer_form.cleaned_data['amount']
                sender_account = Account.objects.get(user=request.user)
                try:
                    target_account = Account.objects.get(user__username=target_username)
                    if amount <= sender_account.balance:
                        sender_account.balance -= amount
                        target_account.balance += amount
                        sender_account.save()
                        target_account.save()
                        Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
                        Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                        return redirect('account_overview')
                    else:
                        return HttpResponse("Insufficient balance.")
                except Account.DoesNotExist:
                    return HttpResponse("Target account does not exist.")

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    })
```