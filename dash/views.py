```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    return HttpResponse("Insufficient funds.", status=400)
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                return redirect('manage_account')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_account = form.cleaned_data['recipient_account']
                if amount > account.balance:
                    return HttpResponse("Insufficient funds.", status=400)
                account.balance -= amount
                recipient_account.balance += amount
                account.save()
                recipient_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer', recipient=recipient_account)
                return redirect('manage_account')

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