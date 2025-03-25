```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_management_view(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('bank_management')
                else:
                    return HttpResponse("Insufficient funds.")

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_username = transfer_form.cleaned_data['recipient']
                account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(user__username=recipient_username)
                if amount <= account.balance:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer to ' + recipient_username)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from ' + request.user.username)
                    return redirect('bank_management')
                else:
                    return HttpResponse("Insufficient funds.")

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    return render(request, 'bank_management.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'balance': Account.objects.get(user=request.user).balance,
    })
```