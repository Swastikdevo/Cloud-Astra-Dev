```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_management_view(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = request.user.account
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('bank_management')
                
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = request.user.account
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('bank_management')
        
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_username = form.cleaned_data['recipient']
                account = request.user.account
                recipient_account = Account.objects.filter(user__username=recipient_username).first()
                
                if recipient_account and amount <= account.balance:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer to ' + recipient_username)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from ' + request.user.username)
                    messages.success(request, f'Transfer of {amount} to {recipient_username} successful!')
                else:
                    messages.error(request, 'Transfer failed. Check recipient and funds!')
                return redirect('bank_management')
                
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()
        transactions = Transaction.objects.filter(account=request.user.account).order_by('-timestamp')

    context = {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
        'account_balance': request.user.account.balance,
    }

    return render(request, 'bank_management.html', context)
```