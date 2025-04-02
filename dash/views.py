```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_dashboard(request):
    # Get the user's account details
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_dashboard')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    return redirect('account_dashboard')
                else:
                    return HttpResponse("Insufficient funds.")
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_account_number = transfer_form.cleaned_data['recipient_account_number']
                transfer_amount = transfer_form.cleaned_data['amount']
                recipient_account = Account.objects.filter(account_number=recipient_account_number).first()

                if recipient_account and transfer_amount <= account.balance:
                    account.balance -= transfer_amount
                    recipient_account.balance += transfer_amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-transfer_amount, transaction_type='Transfer')
                    Transaction.objects.create(account=recipient_account, amount=transfer_amount, transaction_type='Transfer')
                    return redirect('account_dashboard')
                else:
                    return HttpResponse("Transfer failed. Please check account number or insufficient funds.")

    # Initial form handling
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }

    return render(request, 'account/dashboard.html', context)
```