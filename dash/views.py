```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    user_accounts = Account.objects.filter(owner=request.user)
    if request.method == "POST":
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                # Handle account transfer logic
                origin_account = transfer_form.cleaned_data['origin_account']
                destination_account = transfer_form.cleaned_data['destination_account']
                amount = transfer_form.cleaned_data['amount']
                if origin_account.balance >= amount:
                    origin_account.balance -= amount
                    destination_account.balance += amount
                    origin_account.save()
                    destination_account.save()
                    Transaction.objects.create(account=origin_account, amount=-amount, transaction_type='Transfer')
                    Transaction.objects.create(account=destination_account, amount=amount, transaction_type='Transfer')
                    return redirect('account_overview')
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_overview')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                account = withdrawal_form.cleaned_data['account']
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    return redirect('account_overview')

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    
    context = {
        'user_accounts': user_accounts,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    return render(request, 'manage_account.html', context)
```