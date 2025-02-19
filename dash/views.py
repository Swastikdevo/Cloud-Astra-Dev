```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == "POST":
        # Handle deposit
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, type='Deposit')
                return redirect('manage_account')

        # Handle withdrawal
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, type='Withdrawal')
                    return redirect('manage_account')

        # Handle transfer
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient'])
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, type='Transfer', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, type='Transfer', sender=user_account)
                    return redirect('manage_account')

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    return render(request, 'manage_account.html', {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions
    })
```