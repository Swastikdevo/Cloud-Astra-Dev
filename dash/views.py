```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_overview(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                user_account.balance += deposit_form.cleaned_data['amount']
                user_account.save()
                Transaction.objects.create(account=user_account, amount=deposit_form.cleaned_data['amount'], transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('account_overview')

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid() and user_account.balance >= withdraw_form.cleaned_data['amount']:
                user_account.balance -= withdraw_form.cleaned_data['amount']
                user_account.save()
                Transaction.objects.create(account=user_account, amount=withdraw_form.cleaned_data['amount'], transaction_type='Withdrawal')
                messages.success(request, 'Withdrawal successful!')
                return redirect('account_overview')
            else:
                messages.error(request, 'Insufficient balance for withdrawal.')

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient'])
                if user_account.balance >= transfer_form.cleaned_data['amount']:
                    user_account.balance -= transfer_form.cleaned_data['amount']
                    recipient_account.balance += transfer_form.cleaned_data['amount']
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, amount=transfer_form.cleaned_data['amount'], transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=transfer_form.cleaned_data['amount'], transaction_type='Transfer In')
                    messages.success(request, 'Transfer successful!')
                    return redirect('account_overview')
                else:
                    messages.error(request, 'Insufficient balance for transfer.')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    context = {
        'account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'bank/account_overview.html', context)
```