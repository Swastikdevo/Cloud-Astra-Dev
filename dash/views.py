```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, WithdrawForm, DepositForm

@login_required
def account_view(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    if request.method == 'POST':
        transfer_form = TransferForm(request.POST)
        withdraw_form = WithdrawForm(request.POST)
        deposit_form = DepositForm(request.POST)

        if 'transfer' in request.POST and transfer_form.is_valid():
            transfer_amount = transfer_form.cleaned_data['amount']
            recipient_account_number = transfer_form.cleaned_data['recipient_account_number']
            recipient_account = Account.objects.get(account_number=recipient_account_number)

            if user_account.balance >= transfer_amount:
                user_account.balance -= transfer_amount
                recipient_account.balance += transfer_amount
                user_account.save()
                recipient_account.save()

                Transaction.objects.create(account=user_account, amount=-transfer_amount, transaction_type='Transfer')
                Transaction.objects.create(account=recipient_account, amount=transfer_amount, transaction_type='Received')
                return redirect('account')

        elif 'withdraw' in request.POST and withdraw_form.is_valid():
            withdraw_amount = withdraw_form.cleaned_data['amount']
            if user_account.balance >= withdraw_amount:
                user_account.balance -= withdraw_amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=-withdraw_amount, transaction_type='Withdrawal')
                return redirect('account')

        elif 'deposit' in request.POST and deposit_form.is_valid():
            deposit_amount = deposit_form.cleaned_data['amount']
            user_account.balance += deposit_amount
            user_account.save()
            Transaction.objects.create(account=user_account, amount=deposit_amount, transaction_type='Deposit')
            return redirect('account')

    else:
        transfer_form = TransferForm()
        withdraw_form = WithdrawForm()
        deposit_form = DepositForm()

    context = {
        'account': user_account,
        'transactions': transactions,
        'transfer_form': transfer_form,
        'withdraw_form': withdraw_form,
        'deposit_form': deposit_form,
    }
    return render(request, 'account.html', context)
```