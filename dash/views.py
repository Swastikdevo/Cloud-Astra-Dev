```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def manage_account(request):
    account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                transaction = Transaction(account=account, amount=amount, transaction_type='Deposit')
                transaction.save()
                messages.success(request, f'Deposited ${amount:.2f} to your account.')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds for withdrawal.')
                else:
                    account.balance -= amount
                    account.save()
                    transaction = Transaction(account=account, amount=amount, transaction_type='Withdrawal')
                    transaction.save()
                    messages.success(request, f'Withdrew ${amount:.2f} from your account.')
                return redirect('manage_account')
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account_number = form.cleaned_data['recipient_account_number']
                amount = form.cleaned_data['amount']
                recipient_account = Account.objects.filter(account_number=recipient_account_number).first()
                
                if recipient_account is None:
                    messages.error(request, 'Recipient account does not exist.')
                elif amount > account.balance:
                    messages.error(request, 'Insufficient funds for transfer.')
                else:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    transaction = Transaction(account=account, amount=amount, transaction_type='Transfer', recipient=recipient_account)
                    transaction.save()
                    messages.success(request, f'Transferred ${amount:.2f} to account {recipient_account_number}.')
                return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()
    
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    return render(request, 'bank/manage_account.html', context)
```