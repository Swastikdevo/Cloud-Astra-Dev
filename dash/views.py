```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_overview.html', {
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
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        messages.success(request, 'Deposit successful!')
        return redirect('account_overview')
    messages.error(request, 'Invalid deposit amount.')
    return redirect('account_overview')

@login_required
@require_POST
def withdraw(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            messages.success(request, 'Withdrawal successful!')
        else:
            messages.error(request, 'Insufficient balance.')
    else:
        messages.error(request, 'Invalid withdrawal amount.')
    return redirect('account_overview')

@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {
        'transactions': transactions,
    })
```