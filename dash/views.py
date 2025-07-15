```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    account = get_object_or_404(Account, owner=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                    return redirect('manage_account')
                else:
                    messages.error(request, 'Insufficient funds!')
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = get_object_or_404(Account, account_number=form.cleaned_data['recipient_account_number'])
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer to {}'.format(recipient_account.owner.username))
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from {}'.format(account.owner.username))
                    messages.success(request, 'Transfer successful!')
                    return redirect('manage_account')
                else:
                    messages.error(request, 'Insufficient funds!')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()
    
    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/manage_account.html', context)
```