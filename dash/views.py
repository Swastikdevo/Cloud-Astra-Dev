```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'Deposit of ${amount} successful!')
                return redirect('manage_account', account_id=account.id)
                
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds.')
                else:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, f'Withdrawal of ${amount} successful!')
                    return redirect('manage_account', account_id=account.id)

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_id = form.cleaned_data['recipient_id']
                recipient_account = Account.objects.get(id=recipient_id)
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds.')
                else:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='transfer_out', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in', sender=account)
                    messages.success(request, f'Transfer of ${amount} to account {recipient_account.id} successful!')
                    return redirect('manage_account', account_id=account.id)
        
    else:
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