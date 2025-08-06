```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm


@login_required
@require_http_methods(["GET", "POST"])
def banking_operations(request):
    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount} successfully!')
                return redirect('banking_operations')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrew ${amount} successfully!')
                else:
                    messages.error(request, 'Insufficient balance!')
                return redirect('banking_operations')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_username = form.cleaned_data['recipient']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    sender_account = Account.objects.get(user=request.user)
                    if sender_account.balance >= amount:
                        sender_account.balance -= amount
                        recipient_account.balance += amount
                        sender_account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                        messages.success(request, f'Transferred ${amount} to {recipient_username} successfully!')
                    else:
                        messages.error(request, 'Insufficient balance!')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist!')
                return redirect('banking_operations')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    
    return render(request, 'banking/banking_operations.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    })
```