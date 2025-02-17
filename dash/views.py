```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_operations_view(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('bank_operations')

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_operations')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_username = transfer_form.cleaned_data['recipient']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    account = Account.objects.get(user=request.user)
                    if account.balance >= amount:
                        account.balance -= amount
                        recipient_account.balance += amount
                        account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer - Sent')
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer - Received')
                        messages.success(request, 'Transfer successful!')
                    else:
                        messages.error(request, 'Insufficient funds for transfer.')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist.')
                return redirect('bank_operations')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'account': account,
        'transactions': transactions
    }
    return render(request, 'bank_operations.html', context)
```