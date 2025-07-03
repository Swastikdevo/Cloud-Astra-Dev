```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_summary(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
    return render(request, 'account_summary.html', {'accounts': accounts, 'transactions': transactions})

@login_required
@require_POST
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        if account.user == request.user:
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, 'Deposit successful!')
        else:
            messages.error(request, 'You do not have permission to deposit in this account.')
    else:
        messages.error(request, 'Invalid deposit details.')
    return redirect('account_summary')

@login_required
@require_POST
def withdraw(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        if account.user == request.user and account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
            messages.success(request, 'Withdrawal successful!')
        else:
            messages.error(request, 'Invalid withdrawal attempt or insufficient funds.')
    else:
        messages.error(request, 'Invalid withdrawal details.')
    return redirect('account_summary')

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        from_account = form.cleaned_data['from_account']
        to_account = form.cleaned_data['to_account']
        amount = form.cleaned_data['amount']
        if from_account.user == request.user and from_account.balance >= amount and to_account != from_account:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, amount=-amount, transaction_type='transfer')
            Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer')
            messages.success(request, 'Transfer successful!')
        else:
            messages.error(request, 'Invalid transfer details or insufficient funds.')
    else:
        messages.error(request, 'Invalid transfer form.')
    return redirect('account_summary')
```