```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@require_GET
def account_overview(request, account_id):
    account = Account.objects.get(pk=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/account_overview.html', context)

@require_POST
def deposit(request, account_id):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(pk=account_id)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, type='deposit')
        return redirect('account_overview', account_id=account.id)
    return render(request, 'bank/deposit.html', {'form': form})

@require_POST
def withdraw(request, account_id):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(pk=account_id)
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, type='withdrawal')
            return redirect('account_overview', account_id=account.id)
        else:
            return HttpResponse("Insufficient funds", status=400)
    return render(request, 'bank/withdraw.html', {'form': form})

@require_POST
def transfer(request, account_id):
    form = TransferForm(request.POST)
    if form.is_valid():
        target_account_id = form.cleaned_data['target_account_id']
        amount = form.cleaned_data['amount']
        source_account = Account.objects.get(pk=account_id)
        target_account = Account.objects.get(pk=target_account_id)

        if amount <= source_account.balance:
            source_account.balance -= amount
            target_account.balance += amount
            source_account.save()
            target_account.save()
            Transaction.objects.create(account=source_account, amount=-amount, type='transfer', target_account=target_account)
            Transaction.objects.create(account=target_account, amount=amount, type='transfer_received', source_account=source_account)
            return redirect('account_overview', account_id=source_account.id)
        else:
            return HttpResponse("Insufficient funds", status=400)
    return render(request, 'bank/transfer.html', {'form': form})
```