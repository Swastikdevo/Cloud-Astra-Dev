```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('bank_dashboard')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                account = withdrawal_form.cleaned_data['account']
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('bank_dashboard')
                else:
                    return HttpResponse("Insufficient funds")

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                source_account = transfer_form.cleaned_data['source_account']
                target_account = transfer_form.cleaned_data['target_account']
                amount = transfer_form.cleaned_data['amount']
                if source_account.balance >= amount:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(account=source_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                    return redirect('bank_dashboard')
                else:
                    return HttpResponse("Insufficient funds for transfer")

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    context = {
        'user_accounts': user_accounts,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'bank/dashboard.html', context)
```