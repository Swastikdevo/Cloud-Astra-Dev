```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_management_view(request):
    user_accounts = Account.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('bank_management')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return redirect('bank_management')
                else:
                    return HttpResponse("Insufficient funds")

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                source_account = form.cleaned_data['source_account']
                target_account = form.cleaned_data['target_account']
                amount = form.cleaned_data['amount']
                if source_account.balance >= amount:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(account=source_account, amount=amount, transaction_type='Transfer')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer')
                    return redirect('bank_management')
                else:
                    return HttpResponse("Insufficient funds for transfer")
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'user_accounts': user_accounts,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank_management.html', context)
```