```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': user_accounts})

@login_required
def deposit_money(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return redirect('account_dashboard')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw_money(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                return redirect('account_dashboard')
            else:
                return HttpResponse("Insufficient funds", status=400)
    else:
        form = WithdrawalForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer_money(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient_username']
            amount = form.cleaned_data['amount']
            recipient = User.objects.get(username=recipient_username)

            if amount <= account.balance:
                account.balance -= amount
                account.save()
                recipient_account = Account.objects.get(owner=recipient)
                recipient_account.balance += amount
                recipient_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='transfer')
                return redirect('account_dashboard')
            else:
                return HttpResponse("Insufficient funds", status=400)
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form, 'account': account})
```