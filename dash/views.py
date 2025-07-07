```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposit of {amount} successful!')
                return redirect('manage_account')
        
        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrawal of {amount} successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('manage_account')
        
        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                try:
                    recipient_account = Account.objects.get(username=recipient)
                    if account.balance >= amount:
                        account.balance -= amount
                        recipient_account.balance += amount
                        account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer')
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Received Transfer')
                        messages.success(request, f'Transfer of {amount} to {recipient} successful!')
                    else:
                        messages.error(request, 'Insufficient funds.')
                except Account.DoesNotExist:
                    messages.error(request, 'Recipient account does not exist.')
                return redirect('manage_account')
        else:
            messages.error(request, 'Invalid action.')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    return render(request, 'manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    })
```