```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm
from django.contrib import messages


@login_required
def bank_management_view(request):
    # Initialize context dictionary to hold data for rendering templates
    context = {
        'accounts': Account.objects.filter(owner=request.user),
        'transactions': Transaction.objects.filter(account__owner=request.user).order_by('-date'),
    }

    # Handle deposit
    if request.method == 'POST' and 'deposit' in request.POST:
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = form.cleaned_data['account']
            if account.owner == request.user:
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
            else:
                messages.error(request, 'Account ownership mismatch.')
            return redirect('bank_management')

    # Handle withdrawal
    elif request.method == 'POST' and 'withdraw' in request.POST:
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = form.cleaned_data['account']
            if account.owner == request.user and account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                messages.success(request, 'Withdrawal successful!')
            else:
                messages.error(request, 'Insufficient balance or ownership mismatch.')
            return redirect('bank_management')

    # Handle transfer
    elif request.method == 'POST' and 'transfer' in request.POST:
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            if from_account.owner == request.user and from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                messages.success(request, 'Transfer successful!')
            else:
                messages.error(request, 'Insufficient balance or ownership mismatch.')
            return redirect('bank_management')

    # Populate forms for deposits, withdrawals, and transfers
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    context.update({
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })

    return render(request, 'bank_management.html', context)
```