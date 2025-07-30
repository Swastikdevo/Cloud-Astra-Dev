```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_dashboard(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount:.2f} successfully!')
                return redirect('account_dashboard')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount > user_account.balance:
                    messages.error(request, 'Insufficient funds for withdrawal.')
                else:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrew ${amount:.2f} successfully!')
                    return redirect('account_dashboard')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                target_account_number = transfer_form.cleaned_data['account_number']
                amount = transfer_form.cleaned_data['amount']
                try:
                    target_account = Account.objects.get(account_number=target_account_number)
                    if amount > user_account.balance:
                        messages.error(request, 'Insufficient funds for transfer.')
                    else:
                        user_account.balance -= amount
                        target_account.balance += amount
                        user_account.save()
                        target_account.save()
                        Transaction.objects.create(account=user_account, amount=amount, transaction_type='Transfer to ' + target_account_number)
                        Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer from ' + user_account.account_number)
                        messages.success(request, f'Transferred ${amount:.2f} to account {target_account_number} successfully!')
                        return redirect('account_dashboard')
                except Account.DoesNotExist:
                    messages.error(request, 'Target account does not exist.')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    context = {
        'user_account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'account/dashboard.html', context)
```