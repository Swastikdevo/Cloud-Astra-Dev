```python
from django.shortcuts import render, redirect, get_object_or_404
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
                account = get_object_or_404(Account, pk=deposit_form.cleaned_data['account_id'])
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('bank_dashboard')
        
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = get_object_or_404(Account, pk=withdraw_form.cleaned_data['account_id'])
                amount = withdraw_form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds!')
                else:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    messages.success(request, 'Withdrawal successful!')
                return redirect('bank_dashboard')
        
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                source_account = get_object_or_404(Account, pk=transfer_form.cleaned_data['source_account_id'])
                target_account = get_object_or_404(Account, pk=transfer_form.cleaned_data['target_account_id'])
                amount = transfer_form.cleaned_data['amount']
                if amount > source_account.balance:
                    messages.error(request, 'Insufficient funds for transfer!')
                else:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(account=source_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, 'Transfer successful!')
                return redirect('bank_dashboard')

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