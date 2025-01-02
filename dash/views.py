```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_management_view(request):
    user_account = Account.objects.get(user=request.user)
    recent_transactions = Transaction.objects.filter(account=user_account).order_by('-date')[:5]

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Successfully deposited {amount}.')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Successfully withdrew {amount}.')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_management')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                recipient_account = Account.objects.filter(user__username=recipient_username).first()

                if recipient_account and user_account.balance >= amount:
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Transfer', recipient=recipient_account)
                    messages.success(request, f'Successfully transferred {amount} to {recipient_username}.')
                elif not recipient_account:
                    messages.error(request, 'Recipient account does not exist.')
                else:
                    messages.error(request, 'Insufficient funds for transfer.')
                return redirect('bank_management')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    context = {
        'user_account': user_account,
        'recent_transactions': recent_transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'bank_management.html', context)
```