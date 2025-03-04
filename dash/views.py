```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited: ${amount:.2f}')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrew: ${amount:.2f}')
                else:
                    messages.error(request, 'Insufficient balance')
                return redirect('manage_account')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_username = transfer_form.cleaned_data['recipient']
                amount = transfer_form.cleaned_data['amount']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    if user_account.balance >= amount:
                        user_account.balance -= amount
                        recipient_account.balance += amount
                        user_account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=user_account, amount=amount, transaction_type='Transfer Out')
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                        messages.success(request, f'Transferred: ${amount:.2f} to {recipient_username}')
                    else:
                        messages.error(request, 'Insufficient balance for transfer')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient does not exist')
                return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    context = {
        'account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/manage_account.html', context)
```