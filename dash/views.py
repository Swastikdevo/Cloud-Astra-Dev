```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': user_accounts})

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
            return redirect('bank:dashboard')
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
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                return redirect('bank:dashboard')
            else:
                form.add_error('amount', 'Insufficient balance')
    else:
        form = WithdrawForm()
    
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transfer_money(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_account = Account.objects.get(account_number=form.cleaned_data['recipient_account_number'])
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                recipient_account.balance += amount
                account.save()
                recipient_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='transfer', recipient=recipient_account)
                return redirect('bank:dashboard')
            else:
                form.add_error('amount', 'Insufficient balance')
    else:
        form = TransferForm()
    
    return render(request, 'bank/transfer.html', {'form': form, 'account': account})
```