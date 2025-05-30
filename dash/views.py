```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages

@login_required
def account_overview(request):
    account = get_object_or_404(Account, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('account_overview')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('account_overview')
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account_number = form.cleaned_data['recipient_account_number']
                amount = form.cleaned_data['amount']
                recipient_account = get_object_or_404(Account, account_number=recipient_account_number)
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer to ' + recipient_account_number)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from ' + account.account_number)
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('account_overview')
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