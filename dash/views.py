```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    context = {
        'user_accounts': user_accounts,
    }
    return render(request, 'bank/account_dashboard.html', context)

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
            return redirect('account_dashboard')
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                return JsonResponse({'error': 'Insufficient funds!'}, status=400)
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
            return redirect('account_dashboard')
    else:
        form = WithdrawalForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            target_account_id = form.cleaned_data['target_account']
            amount = form.cleaned_data['amount']
            target_account = Account.objects.get(id=target_account_id)

            if amount > account.balance:
                return JsonResponse({'error': 'Insufficient funds!'}, status=400)
            account.balance -= amount
            target_account.balance += amount
            account.save()
            target_account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer to {}'.format(target_account.account_number))
            Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer from {}'.format(account.account_number))
            return redirect('account_dashboard')
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form, 'account': account})
```