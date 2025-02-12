```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_management_view(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'You have successfully deposited {amount}.')
                return redirect('bank_management')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'You have successfully withdrawn {amount}.')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_management')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                transfer_to = form.cleaned_data['transfer_to']
                amount = form.cleaned_data['amount']
                try:
                    recipient_account = Account.objects.get(account_number=transfer_to)
                    if amount <= user_account.balance:
                        user_account.balance -= amount
                        recipient_account.balance += amount
                        user_account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=user_account, amount=amount, transaction_type='Transfer Out')
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                        messages.success(request, f'You have successfully transferred {amount} to {transfer_to}.')
                    else:
                        messages.error(request, 'Insufficient funds.')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist.')
                return redirect('bank_management')
    
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    return render(request, 'bank_management.html', {
        'account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })
```