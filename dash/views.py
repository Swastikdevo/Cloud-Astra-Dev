```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

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
                messages.success(request, f'Successfully deposited ${amount:.2f}')
                return redirect('account_dashboard')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Successfully withdrew ${amount:.2f}')
                else:
                    messages.error(request, 'Insufficient balance for withdrawal.')
                return redirect('account_dashboard')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                recipient_account = transfer_form.cleaned_data['recipient_account']
                amount = transfer_form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, f'Successfully transferred ${amount:.2f} to {recipient_account.user.username}')
                else:
                    messages.error(request, 'Insufficient balance for transfer.')
                return redirect('account_dashboard')
    else:
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
    return render(request, 'bank/account_dashboard.html', context)
```