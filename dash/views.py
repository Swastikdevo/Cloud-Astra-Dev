```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    if request.method == "POST":
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'${amount} deposited successfully!')
                return redirect('account_management')

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
                    messages.success(request, f'${amount} withdrawn successfully!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('account_management')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_username = transfer_form.cleaned_data['recipient']
                account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.filter(user__username=recipient_username).first()
                if recipient_account and account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer', sender=account)
                    messages.success(request, f'${amount} transferred to {recipient_username} successfully!')
                else:
                    messages.error(request, 'Transfer failed. Check recipient username or insufficient funds.')
                return redirect('account_management')

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    return render(request, 'account_management.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    })
```