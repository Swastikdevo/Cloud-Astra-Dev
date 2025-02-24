```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_view(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'Deposited: ${amount:.2f} successfully!')
                return redirect('account_view', account_id=account.id)
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                    messages.success(request, f'Withdrew: ${amount:.2f} successfully!')
                else:
                    messages.error(request, 'Insufficient balance for this withdrawal.')
                return redirect('account_view', account_id=account.id)
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_account_id = transfer_form.cleaned_data['recipient_account_id']
                amount = transfer_form.cleaned_data['amount']
                
                if amount <= account.balance:
                    recipient_account = get_object_or_404(Account, id=recipient_account_id)
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='transfer', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer', sender=account)
                    messages.success(request, f'Transferred: ${amount:.2f} to account #{recipient_account_id} successfully!')
                else:
                    messages.error(request, 'Insufficient balance for this transfer.')
                return redirect('account_view', account_id=account.id)

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    transactions = Transaction.objects.filter(account=account).order_by('-date_created')
    
    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    
    return render(request, 'account_detail.html', context)
```