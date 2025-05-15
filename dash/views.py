```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_dashboard(request):
    account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                messages.success(request, f'Deposited ${amount} successfully!')
                return redirect('bank_dashboard')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    messages.success(request, f'Withdrew ${amount} successfully!')
                    return redirect('bank_dashboard')
                else:
                    messages.error(request, 'Insufficient funds!')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_username = transfer_form.cleaned_data['recipient']
                if amount <= account.balance:
                    try:
                        recipient_account = Account.objects.get(user__username=recipient_username)
                        account.balance -= amount
                        recipient_account.balance += amount
                        account.save()
                        recipient_account.save()
                        messages.success(request, f'Transferred ${amount} to {recipient_username} successfully!')
                        return redirect('bank_dashboard')
                    except Account.DoesNotExist:
                        messages.error(request, 'Recipient account does not exist!')
                else:
                    messages.error(request, 'Insufficient funds!')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/dashboard.html', context)
```