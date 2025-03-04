```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@csrf_exempt
def bank_management_view(request):
    # Handle the deposit action
    if request.method == 'POST' and 'deposit' in request.POST:
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('bank_management')

    # Handle the withdrawal action
    elif request.method == 'POST' and 'withdraw' in request.POST:
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return redirect('bank_management')

    # Handle the money transfer action
    elif request.method == 'POST' and 'transfer' in request.POST:
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            sender_account = Account.objects.get(user=request.user)
            recipient_account = Account.objects.get(user__username=recipient_username)
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()
                Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer')
                return redirect('bank_management')

    # Render the bank management page with forms
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')

    return render(request, 'bank_management.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions
    })
```