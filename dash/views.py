```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                account.balance += amount
                account.save()
                messages.success(request, 'Deposit successful.')
                return redirect('bank_dashboard')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = withdraw_form.cleaned_data['account']
                amount = withdraw_form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    account.balance -= amount
                    account.save()
                    messages.success(request, 'Withdrawal successful.')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_dashboard')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                from_account = transfer_form.cleaned_data['from_account']
                to_account = transfer_form.cleaned_data['to_account']
                amount = transfer_form.cleaned_data['amount']
                if from_account.balance >= amount:
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer_in')
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    messages.success(request, 'Transfer successful.')
                else:
                    messages.error(request, 'Insufficient funds for transfer.')
                return redirect('bank_dashboard')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'user_accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/dashboard.html', context)
```