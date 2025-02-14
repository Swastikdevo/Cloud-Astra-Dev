```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    context = {
        'accounts': user_accounts,
        'total_balance': sum(account.balance for account in user_accounts),
    }
    return render(request, 'bank/account_dashboard.html', context)

@login_required
def deposit_money(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('account_dashboard')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw_money(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
            return redirect('account_dashboard')
    else:
        form = WithdrawForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer_money(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            source_account = Account.objects.get(id=form.cleaned_data['source_account_id'], owner=request.user)
            target_account = Account.objects.get(id=form.cleaned_data['target_account_id'])
            amount = form.cleaned_data['amount']
            if amount > source_account.balance:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
            source_account.balance -= amount
            target_account.balance += amount
            source_account.save()
            target_account.save()
            Transaction.objects.create(account=source_account, amount=-amount, transaction_type='Transfer')
            Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer')
            return redirect('account_dashboard')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form})
```