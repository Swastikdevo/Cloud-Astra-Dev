```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def account_view(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = Account.objects.get(account_number=form.cleaned_data['recipient'])
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    # Create transaction
                    Transaction.objects.create(
                        sender=user_account,
                        recipient=recipient_account,
                        amount=amount,
                        transaction_type='Transfer'
                    )
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    return redirect('bank:account_view')
        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(
                    account=user_account,
                    amount=amount,
                    transaction_type='Deposit'
                )
                return redirect('bank:account_view')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(
                        account=user_account,
                        amount=amount,
                        transaction_type='Withdrawal'
                    )
                    return redirect('bank:account_view')

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transactions = Transaction.objects.filter(account=user_account)

    context = {
        'account': user_account,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    }

    return render(request, 'bank/account_view.html', context)
```