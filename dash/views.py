```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'${amount} deposited successfully!')
                return redirect('manage_account', account_id=account_id)
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, f'${amount} withdrawn successfully!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account', account_id=account_id)
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account_id = form.cleaned_data['recipient_account']
                amount = form.cleaned_data['amount']
                recipient_account = get_object_or_404(Account, id=recipient_account_id)

                if amount <= account.balance:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in')
                    messages.success(request, f'${amount} transferred to account #{recipient_account_id} successfully!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account', account_id=account_id)

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