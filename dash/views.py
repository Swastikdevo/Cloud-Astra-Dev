```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                transfer_funds(account, form.cleaned_data['amount'], form.cleaned_data['recipient_account'])
                return redirect('account_overview')
        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account.balance += form.cleaned_data['amount']
                account.save()
                return redirect('account_overview')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                withdraw_funds(account, form.cleaned_data['amount'])
                return redirect('account_overview')

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    context = {
        'account': account,
        'transactions': transactions,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }

    return render(request, 'bank/account_overview.html', context)

@require_POST
def transfer_funds(account, amount, recipient_account_number):
    recipient_account = Account.objects.get(account_number=recipient_account_number)
    if account.balance >= amount:
        account.balance -= amount
        recipient_account.balance += amount
        account.save()
        recipient_account.save()
        Transaction.objects.create(account=account, amount=-amount, type='transfer', date=timezone.now())
        Transaction.objects.create(account=recipient_account, amount=amount, type='transfer', date=timezone.now())
    else:
        raise ValueError("Insufficient funds for the transfer.")

@require_POST
def withdraw_funds(account, amount):
    if account.balance >= amount:
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=-amount, type='withdraw', date=timezone.now())
    else:
        raise ValueError("Insufficient funds for the withdrawal.")
```