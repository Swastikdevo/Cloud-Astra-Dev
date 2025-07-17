```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@csrf_exempt
@login_required
def bank_management_view(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount} successfully!')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds!')
                else:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    messages.success(request, f'Withdrew ${amount} successfully!')
                return redirect('bank_management')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                recipient_account = Account.objects.filter(user__username=recipient_username).first()
                
                if not recipient_account:
                    messages.error(request, 'Recipient not found!')
                elif amount > account.balance:
                    messages.error(request, 'Insufficient funds!')
                else:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer to {}'.format(recipient_username))
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from {}'.format(request.user.username))
                    messages.success(request, f'Transferred ${amount} to {recipient_username} successfully!')
                return redirect('bank_management')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date_created')

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    return render(request, 'bank_management.html', context)
```