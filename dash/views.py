```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import BankAccount, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib import messages

@login_required
def manage_account(request):
    account = get_object_or_404(BankAccount, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                    return redirect('manage_account')
                else:
                    messages.error(request, 'Insufficient funds!')
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account_number = form.cleaned_data['recipient_account']
                amount = form.cleaned_data['amount']
                recipient_account = get_object_or_404(BankAccount, account_number=recipient_account_number)
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, 'Transfer successful!')
                    return redirect('manage_account')
                else:
                    messages.error(request, 'Insufficient funds!')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/manage_account.html', context)
```