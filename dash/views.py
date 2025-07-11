```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_management_view(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount} successfully.')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrew ${amount} successfully.')
                else:
                    messages.error(request, 'Insufficient balance.')
                return redirect('bank_management')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                target_username = form.cleaned_data['target_user']
                account = Account.objects.get(user=request.user)
                target_account = Account.objects.get(user__username=target_username)
                
                if account.balance >= amount:
                    account.balance -= amount
                    target_account.balance += amount
                    account.save()
                    target_account.save()
                    Transaction.objects.create(account=account, target_account=target_account, amount=amount, transaction_type='Transfer')
                    messages.success(request, f'Transferred ${amount} to {target_username} successfully.')
                else:
                    messages.error(request, 'Insufficient balance.')
                return redirect('bank_management')

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()
    
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    return render(request, 'bank_management.html', context)
```