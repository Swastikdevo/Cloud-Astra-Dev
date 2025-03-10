```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.contrib import messages

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': user_accounts})

@login_required
def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, f'Deposited ${amount} successfully!')
            return redirect('account_overview')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                messages.error(request, 'Insufficient funds!')
            else:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                messages.success(request, f'Withdrew ${amount} successfully!')
                return redirect('account_overview')
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request, account_id):
    source_account = get_object_or_404(Account, id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            target_account_id = form.cleaned_data['target_account_id']
            amount = form.cleaned_data['amount']

            target_account = get_object_or_404(Account, id=target_account_id)
            if amount > source_account.balance:
                messages.error(request, 'Insufficient funds for transfer!')
            else:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                Transaction.objects.create(account=source_account, amount=amount, transaction_type='transfer_out')
                Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer_in')
                messages.success(request, f'Transferred ${amount} successfully!')
                return redirect('account_overview')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form, 'account': source_account})
```