```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, AccountForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': user_accounts})

@login_required
def deposit_funds(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, f'Successfully deposited ${amount} to your account.')
            return redirect('bank:bank_dashboard')
    else:
        form = DepositForm()

    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw_funds(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                messages.success(request, f'Successfully withdrew ${amount} from your account.')
                return redirect('bank:bank_dashboard')
            else:
                messages.error(request, 'Insufficient funds.')
    else:
        form = WithdrawForm()

    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.owner = request.user
            new_account.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('bank:bank_dashboard')
    else:
        form = AccountForm()

    return render(request, 'bank/create_account.html', {'form': form})
```