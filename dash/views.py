```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_management_view(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Withdraw')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_management')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                receiver_username = transfer_form.cleaned_data['receiver']
                amount = transfer_form.cleaned_data['amount']
                receiver_account = Account.objects.filter(user__username=receiver_username).first()
                if receiver_account and amount <= user_account.balance:
                    user_account.balance -= amount
                    receiver_account.balance += amount
                    user_account.save()
                    receiver_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Transfer')
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='Receive')
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Transfer failed. Check the account and balance.')
                return redirect('bank_management')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')[:10]
    
    context = {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    return render(request, 'bank_management.html', context)
```