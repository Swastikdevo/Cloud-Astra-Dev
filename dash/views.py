```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@require_GET
def account_summary(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_summary.html', {
        'account': account,
        'transactions': transactions,
    })

@login_required
@require_POST
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        messages.success(request, 'Deposit successful!')
        return redirect('account_summary')
    else:
        messages.error(request, 'Deposit failed. Please correct the errors.')
        return redirect('account_summary')

@login_required
@require_POST
def withdraw(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
            messages.success(request, 'Withdrawal successful!')
            return redirect('account_summary')
        else:
            messages.error(request, 'Insufficient funds for this withdrawal.')
            return redirect('account_summary')
    else:
        messages.error(request, 'Withdrawal failed. Please correct the errors.')
        return redirect('account_summary')

@login_required
@require_GET
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {
        'transactions': transactions,
    })
```