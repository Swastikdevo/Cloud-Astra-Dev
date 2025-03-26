```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_management(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = Account.objects.get(account_number=form.cleaned_data['recipient'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(
                        sender=account,
                        recipient=recipient_account,
                        amount=amount,
                        transaction_type='transfer'
                    )
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('account_management')

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='deposit'
                )
                messages.success(request, 'Deposit successful!')
                return redirect('account_management')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        amount=amount,
                        transaction_type='withdrawal'
                    )
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('account_management')

    context = {
        'account': account,
        'transfer_form': TransferForm(),
        'deposit_form': DepositForm(),
        'withdrawal_form': WithdrawalForm(),
    }
    return render(request, 'account_management.html', context)
```