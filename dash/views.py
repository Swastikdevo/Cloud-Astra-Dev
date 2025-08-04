```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

@login_required
def account_view(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_view')

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
                    return redirect('account_view')

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient_username']
                amount = form.cleaned_data['amount']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    if amount <= account.balance:
                        with transaction.atomic():
                            account.balance -= amount
                            recipient_account.balance += amount
                            account.save()
                            recipient_account.save()
                            Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer', sender=account)
                        return redirect('account_view')
                except ObjectDoesNotExist:
                    form.add_error('recipient_username', 'Recipient account does not exist.')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    
    return render(request, 'bank/account_view.html', context)
```