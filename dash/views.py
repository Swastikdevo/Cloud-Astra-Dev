```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_view(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    Account.objects.get(user__username=recipient).balance += amount
                    Transaction.objects.create(account=account, type='transfer', amount=amount, recipient=recipient)
                    account.save()
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds!')

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                Transaction.objects.create(account=account, type='deposit', amount=amount)
                account.save()
                messages.success(request, 'Deposit successful!')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    Transaction.objects.create(account=account, type='withdrawal', amount=amount)
                    account.save()
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    }
    return render(request, 'bank/account.html', context)
```