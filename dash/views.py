```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient_account_number'])
                amount = transfer_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, type='Transfer', amount=amount)
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient balance for this transfer.')
                return redirect('manage_account')
        
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, type='Deposit', amount=amount)
                messages.success(request, 'Deposit successful!')
                return redirect('manage_account')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, type='Withdrawal', amount=amount)
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient balance for this withdrawal.')
                return redirect('manage_account')

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    context = {
        'account': user_account,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    }

    return render(request, 'bank/manage_account.html', context)
```