```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    total_balance = sum(account.balance for account in user_accounts)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')[:5]

    return render(request, 'bank/account_overview.html', {
        'user_accounts': user_accounts,
        'total_balance': total_balance,
        'transactions': transactions,
    })

@login_required
def deposit(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('account_overview')
    else:
        form = DepositForm()

    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                return redirect('account_overview')
            else:
                return HttpResponse("Insufficient funds.")
    else:
        form = WithdrawForm()

    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            target_account = form.cleaned_data['target_account']
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                target_account.balance += amount
                account.save()
                target_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                return redirect('account_overview')
            else:
                return HttpResponse("Insufficient funds.")
    else:
        form = TransferForm()

    return render(request, 'bank/transfer.html', {'form': form, 'account': account})
```