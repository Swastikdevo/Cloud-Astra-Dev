```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

@login_required
def account_dashboard(request):
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
                messages.success(request, 'Deposit successful!')
                return redirect('account_dashboard')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
                    messages.success(request, 'Withdrawal successful!')
                    return redirect('account_dashboard')
                else:
                    messages.error(request, 'Insufficient funds!')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_username = transfer_form.cleaned_data['recipient']
                transfer_amount = transfer_form.cleaned_data['amount']
                recipient_account = Account.objects.filter(user__username=recipient_username).first()
                
                if recipient_account and transfer_amount <= account.balance:
                    account.balance -= transfer_amount
                    recipient_account.balance += transfer_amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-transfer_amount, transaction_type='Transfer to {}'.format(recipient_username))
                    Transaction.objects.create(account=recipient_account, amount=transfer_amount, transaction_type='Transfer from {}'.format(request.user.username))
                    messages.success(request, 'Transfer successful!')
                    return redirect('account_dashboard')
                else:
                    messages.error(request, 'Transfer failed! Check recipient username or insufficient funds.')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/account_dashboard.html', context)
```