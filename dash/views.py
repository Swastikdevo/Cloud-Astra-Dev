```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, WithdrawalForm, DepositForm

@login_required
@csrf_exempt
def manage_account(request):
    context = {}

    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_account = transfer_form.cleaned_data['recipient_account']
                sender_account = Account.objects.get(user=request.user)

                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()

                    Transaction.objects.create(
                        account=sender_account,
                        amount=-amount,
                        transaction_type='Transfer to {}'.format(recipient_account.account_number)
                    )
                    Transaction.objects.create(
                        account=recipient_account,
                        amount=amount,
                        transaction_type='Transfer from {}'.format(sender_account.account_number)
                    )
                    context['message'] = 'Transfer successful!'
                else:
                    context['error'] = 'Insufficient funds for the transfer.'
        
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
                        amount=-amount,
                        transaction_type='Withdrawal'
                    )
                    context['message'] = 'Withdrawal successful!'
                else:
                    context['error'] = 'Insufficient funds for the withdrawal.'

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
                context['message'] = 'Deposit successful!'

    else:
        transfer_form = TransferForm()
        withdrawal_form = WithdrawalForm()
        deposit_form = DepositForm()

    context['transfer_form'] = transfer_form
    context['withdrawal_form'] = withdrawal_form
    context['deposit_form'] = deposit_form

    return render(request, 'account/manage_account.html', context)
```