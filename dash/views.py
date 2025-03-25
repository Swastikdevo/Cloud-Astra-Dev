```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                transfer_amount = form.cleaned_data['amount']
                recipient_account = form.cleaned_data['recipient_account']
                
                # Perform transfer logic
                sender_account = Account.objects.get(user=request.user)
                if sender_account.balance >= transfer_amount:
                    sender_account.balance -= transfer_amount
                    recipient_account.balance += transfer_amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, amount=-transfer_amount, transaction_type='Transfer')
                    Transaction.objects.create(account=recipient_account, amount=transfer_amount, transaction_type='Received')
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient funds for transfer!')
                return redirect('manage_account')

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                deposit_amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += deposit_amount
                account.save()
                Transaction.objects.create(account=account, amount=deposit_amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('manage_account')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                withdraw_amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= withdraw_amount:
                    account.balance -= withdraw_amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-withdraw_amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds for withdrawal!')
                return redirect('manage_account')

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    account_details = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account_details).order_by('-date')

    context = {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'account': account_details,
        'transactions': transactions,
    }
    return render(request, 'bank/manage_account.html', context)
```