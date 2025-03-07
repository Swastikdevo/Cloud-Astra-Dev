```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages

@login_required
def account_summary(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/account_summary.html', context)

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
        messages.success(request, f'Deposited ${amount:.2f} successfully.')
        return redirect('account_summary')
    else:
        messages.error(request, 'Invalid deposit amount.')
    return redirect('account_summary')

@login_required
@require_POST
def withdraw(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if amount <= account.balance:
            account.balance -= amount
            account.save()

            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            messages.success(request, f'Withdrew ${amount:.2f} successfully.')
        else:
            messages.error(request, 'Insufficient funds.')
    else:
        messages.error(request, 'Invalid withdrawal amount.')
    return redirect('account_summary')

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        recipient_username = form.cleaned_data['recipient']
        amount = form.cleaned_data['amount']
        sender_account = Account.objects.get(user=request.user)

        try:
            recipient_account = Account.objects.get(user__username=recipient_username)
            if amount <= sender_account.balance:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()

                Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer_out')
                Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in')

                messages.success(request, f'Transferred ${amount:.2f} to {recipient_username} successfully.')
            else:
                messages.error(request, 'Insufficient funds for transfer.')
        except Account.DoesNotExist:
            messages.error(request, 'Recipient account does not exist.')
    else:
        messages.error(request, 'Invalid transfer details.')
    
    return redirect('account_summary')
```