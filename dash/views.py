```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.contrib import messages

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/account_overview.html', context)

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
    else:
        messages.error(request, 'Error in deposit.')

    return redirect('account_overview')

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
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            messages.success(request, 'Withdrawal successful!')
        else:
            messages.error(request, 'Insufficient funds!')
    else:
        messages.error(request, 'Error in withdrawal.')

    return redirect('account_overview')

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        recipient_account_number = form.cleaned_data['recipient_account_number']
        sender_account = Account.objects.get(user=request.user)
        recipient_account = Account.objects.get(account_number=recipient_account_number)

        if sender_account.balance >= amount:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()
            Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='transfer')
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer')
            messages.success(request, 'Transfer successful!')
        else:
            messages.error(request, 'Insufficient funds for transfer!')
    else:
        messages.error(request, 'Error in transfer.')

    return redirect('account_overview')
```