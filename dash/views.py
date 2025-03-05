```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposit of {amount} successful!')
                return redirect('manage_account')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrawal of {amount} successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_username = transfer_form.cleaned_data['recipient']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    if amount <= user_account.balance:
                        user_account.balance -= amount
                        recipient_account.balance += amount
                        user_account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Transfer to ' + recipient_username)
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from ' + request.user.username)
                        messages.success(request, f'Transfer of {amount} to {recipient_username} successful!')
                    else:
                        messages.error(request, 'Insufficient funds!')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist!')
                return redirect('manage_account')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    context = {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/manage_account.html', context)
```