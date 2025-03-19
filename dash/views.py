```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_view(request):
    account = get_object_or_404(Account, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'You deposited ${amount:.2f}.')
                return redirect('account_view')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'You withdrew ${amount:.2f}.')
                    return redirect('account_view')
                else:
                    messages.error(request, 'Insufficient funds.')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                target_account_number = transfer_form.cleaned_data['target_account_number']
                amount = transfer_form.cleaned_data['amount']
                if amount <= account.balance:
                    try:
                        target_account = get_object_or_404(Account, account_number=target_account_number)
                        account.balance -= amount
                        target_account.balance += amount
                        account.save()
                        target_account.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                        Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                        messages.success(request, f'You transferred ${amount:.2f} to account {target_account_number}.')
                        return redirect('account_view')
                    except Account.DoesNotExist:
                        messages.error(request, 'Target account does not exist.')
                else:
                    messages.error(request, 'Insufficient funds for transfer.')

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
    return render(request, 'bank/account_view.html', context)
```