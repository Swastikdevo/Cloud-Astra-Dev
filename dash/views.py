```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_overview(request):
    user = request.user
    account = Account.objects.get(user=user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    
    if request.method == 'POST':
        # Handle deposit
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, 'Deposit successful!')
            return redirect('account_overview')
        
        # Handle withdrawal
        withdrawal_form = WithdrawalForm(request.POST)
        if withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                messages.success(request, 'Withdrawal successful!')
                return redirect('account_overview')
            else:
                messages.error(request, 'Insufficient funds.')

        # Handle transfer
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            target_account = transfer_form.cleaned_data['target_account']
            amount = transfer_form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                target_account.balance += amount
                account.save()
                target_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                messages.success(request, 'Transfer successful!')
                return redirect('account_overview')
            else:
                messages.error(request, 'Insufficient funds for transfer.')

    else:
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
    return render(request, 'bank/account_overview.html', context)
```