```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('bank_dashboard')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_dashboard')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                source_account = form.cleaned_data['source_account']
                target_account = form.cleaned_data['target_account']
                if source_account.balance >= amount:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(account=source_account, amount=-amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds for transfer.')
                return redirect('bank_dashboard')
        
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/dashboard.html', context)
```