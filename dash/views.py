```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.db import transaction

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

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
            return JsonResponse({'status': 'success', 'balance': account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
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
            if amount > account.balance:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'}, status=400)
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
            return JsonResponse({'status': 'success', 'balance': account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            source_account = Account.objects.get(id=form.cleaned_data['source_account'], owner=request.user)
            destination_account = Account.objects.get(id=form.cleaned_data['destination_account'])
            amount = form.cleaned_data['amount']

            if amount > source_account.balance:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds in source account'}, status=400)

            with transaction.atomic():
                source_account.balance -= amount
                destination_account.balance += amount
                source_account.save()
                destination_account.save()
                Transaction.objects.create(account=source_account, amount=-amount, transaction_type='Transfer')
                Transaction.objects.create(account=destination_account, amount=amount, transaction_type='Transfer')
                
            return JsonResponse({'status': 'success', 'source_balance': source_account.balance, 'destination_balance': destination_account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form})
```