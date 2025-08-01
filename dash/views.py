```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_management(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Successfully deposited!')
                return redirect('bank_management')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, 'Successfully withdrawn!')
                else:
                    messages.error(request, 'Insufficient balance!')
                return redirect('bank_management')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_username = form.cleaned_data['recipient_username']
                sender_account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(user__username=recipient_username)
                if amount <= sender_account.balance:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='Transfer to ' + recipient_username)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from ' + request.user.username)
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient balance for transfer!')
                return redirect('bank_management')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    context = {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'account': Account.objects.get(user=request.user),
        'transactions': Transaction.objects.filter(account__user=request.user).order_by('-date'),
    }
    
    return render(request, 'bank_management.html', context)
```