```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.utils import timezone

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == "POST":
        transfer_form = TransferForm(request.POST)
        deposit_form = DepositForm(request.POST)
        withdraw_form = WithdrawForm(request.POST)

        if transfer_form.is_valid():
            # Handle money transfer
            source_account = transfer_form.cleaned_data['source_account']
            target_account = transfer_form.cleaned_data['target_account']
            amount = transfer_form.cleaned_data['amount']
            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                Transaction.objects.create(
                    account=source_account,
                    amount=-amount,
                    transaction_type='Transfer',
                    timestamp=timezone.now()
                )
                Transaction.objects.create(
                    account=target_account,
                    amount=amount,
                    transaction_type='Received Transfer',
                    timestamp=timezone.now()
                )
                return redirect('manage_account')

        elif deposit_form.is_valid():
            # Handle deposit
            account = deposit_form.cleaned_data['account']
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='Deposit',
                timestamp=timezone.now()
            )
            return redirect('manage_account')

        elif withdraw_form.is_valid():
            # Handle withdrawal
            account = withdraw_form.cleaned_data['account']
            amount = withdraw_form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    amount=-amount,
                    transaction_type='Withdrawal',
                    timestamp=timezone.now()
                )
                return redirect('manage_account')

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    context = {
        'accounts': accounts,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'bank/manage_account.html', context)
```