```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': user_accounts})

@login_required
@require_POST
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = form.cleaned_data['account']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        messages.success(request, 'Deposit successful!')
    else:
        messages.error(request, 'Error in deposit. Please try again.')
    return redirect('bank_dashboard')

@login_required
@require_POST
def withdraw(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = form.cleaned_data['account']
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
            messages.success(request, 'Withdrawal successful!')
        else:
            messages.error(request, 'Insufficient funds.')
    else:
        messages.error(request, 'Error in withdrawal. Please try again.')
    return redirect('bank_dashboard')

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        from_account = form.cleaned_data['from_account']
        to_account = form.cleaned_data['to_account']
        if from_account.balance >= amount:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
            messages.success(request, 'Transfer successful!')
        else:
            messages.error(request, 'Insufficient funds for transfer.')
    else:
        messages.error(request, 'Error in transfer. Please try again.')
    return redirect('bank_dashboard')
```