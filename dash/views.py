```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = request.user.account
                recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient_account_number'])
                amount = transfer_form.cleaned_data['amount']

                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()

                    Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='Transfer')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer Received')
                    return redirect('account_summary')

        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = request.user.account
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()

                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_summary')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                account = request.user.account
                amount = withdrawal_form.cleaned_data['amount']

                if account.balance >= amount:
                    account.balance -= amount
                    account.save()

                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    return redirect('account_summary')

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'current_balance': request.user.account.balance,
    }
    return render(request, 'bank/manage_account.html', context)
```