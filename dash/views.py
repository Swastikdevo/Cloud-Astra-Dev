```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_view(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, transaction_type='Deposit', amount=amount)
                messages.success(request, 'Deposit successful!')
                return redirect('bank_view')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, transaction_type='Withdraw', amount=amount)
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('bank_view')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    if user_account.balance >= amount:
                        user_account.balance -= amount
                        recipient_account.balance += amount
                        user_account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=user_account, transaction_type='Transfer Out', amount=amount)
                        Transaction.objects.create(account=recipient_account, transaction_type='Transfer In', amount=amount)
                        messages.success(request, f'Transfer to {recipient_username} successful!')
                    else:
                        messages.error(request, 'Insufficient funds!')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist!')
                return redirect('bank_view')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')[:10]

    return render(request, 'bank_view.html', {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    })
```