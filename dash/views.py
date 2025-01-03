```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_accounts(request):
    user = request.user
    accounts = Account.objects.filter(user=user)

    # Handle deposit
    if request.method == 'POST' and 'deposit' in request.POST:
        form = DepositForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, 'Deposit successful!')
            return redirect('manage_accounts')

    # Handle withdrawal
    elif request.method == 'POST' and 'withdraw' in request.POST:
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                messages.success(request, 'Withdrawal successful!')
            else:
                messages.error(request, 'Insufficient balance!')
            return redirect('manage_accounts')

    # Handle transfer
    elif request.method == 'POST' and 'transfer' in request.POST:
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']
            if amount <= from_account.balance:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                messages.success(request, 'Transfer successful!')
            else:
                messages.error(request, 'Insufficient balance!')
            return redirect('manage_accounts')
    
    # Initialize forms
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    context = {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/manage_accounts.html', context)
```