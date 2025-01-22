```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                deposit_amount = form.cleaned_data['amount']
                user_account.balance += deposit_amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=deposit_amount, transaction_type='Deposit')
                return redirect('manage_account')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                withdraw_amount = form.cleaned_data['amount']
                if user_account.balance >= withdraw_amount:
                    user_account.balance -= withdraw_amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=withdraw_amount, transaction_type='Withdrawal')
                else:
                    return HttpResponse('Insufficient funds.')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                transfer_amount = form.cleaned_data['amount']
                target_account_number = form.cleaned_data['target_account']
                try:
                    target_account = Account.objects.get(account_number=target_account_number)
                    if user_account.balance >= transfer_amount:
                        user_account.balance -= transfer_amount
                        target_account.balance += transfer_amount
                        user_account.save()
                        target_account.save()
                        Transaction.objects.create(account=user_account, amount=transfer_amount, transaction_type='Transfer Out')
                        Transaction.objects.create(account=target_account, amount=transfer_amount, transaction_type='Transfer In')
                    else:
                        return HttpResponse('Insufficient funds.')
                except Account.DoesNotExist:
                    return HttpResponse('Target account does not exist.')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    context = {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'bank/manage_account.html', context)
```