```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages

@login_required
def bank_account_view(request):
    account = get_object_or_404(Account, user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('bank_account_view')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('bank_account_view')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                target_account_number = form.cleaned_data['target_account_number']
                amount = form.cleaned_data['amount']
                target_account = get_object_or_404(Account, account_number=target_account_number)

                if amount <= account.balance:
                    account.balance -= amount
                    target_account.balance += amount
                    account.save()
                    target_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds for transfer!')
                return redirect('bank_account_view')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    return render(request, 'bank/account.html', context)
```