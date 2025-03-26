```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                to_account = transfer_form.cleaned_data['to_account']
                # Perform transfer logic
                from_account = Account.objects.get(user=request.user)
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account_instance = Account.objects.get(account_number=to_account)
                    to_account_instance.balance += amount
                    from_account.save()
                    to_account_instance.save()
                    Transaction.objects.create(
                        account=from_account,
                        amount=amount,
                        transaction_type='Transfer'
                    )
                    return HttpResponse("Transfer Successful")
                else:
                    return HttpResponse("Insufficient Funds")
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Deposit'
                )
                return HttpResponse("Deposit Successful")
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        amount=amount,
                        transaction_type='Withdrawal'
                    )
                    return HttpResponse("Withdrawal Successful")
                else:
                    return HttpResponse("Insufficient Funds")
    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'account_management.html', {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```