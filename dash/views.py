```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return redirect('bank:bank_dashboard')
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
@require_POST
def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount > account.balance:
            return HttpResponse("Insufficient funds", status=400)
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
        return redirect('bank:bank_dashboard')
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
@require_POST
def transfer(request, from_account_id, to_account_id):
    from_account = get_object_or_404(Account, id=from_account_id, user=request.user)
    to_account = get_object_or_404(Account, id=to_account_id, user=request.user)
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount > from_account.balance:
            return HttpResponse("Insufficient funds", status=400)
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()
        Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
        Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
        return redirect('bank:bank_dashboard')
    return render(request, 'bank/transfer.html', {'form': form, 'from_account': from_account, 'to_account': to_account})
```