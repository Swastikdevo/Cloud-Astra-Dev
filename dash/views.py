```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposit of ${amount} successful!')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrawal of ${amount} successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('manage_account')
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                recipient = Account.objects.filter(user__username=recipient_username).first()
                if recipient and amount <= user_account.balance:
                    user_account.balance -= amount
                    recipient.balance += amount
                    user_account.save()
                    recipient.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient, amount=amount, transaction_type='Transfer In')
                    messages.success(request, f'Transfer of ${amount} to {recipient_username} successful!')
                else:
                    if not recipient:
                        messages.error(request, 'Recipient account does not exist.')
                    else:
                        messages.error(request, 'Insufficient funds.')
                return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    return render(request, 'bank/manage_account.html', {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })
```