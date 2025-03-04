```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'You have successfully deposited ${amount}.')
                return redirect('manage_account')
        
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds for withdrawal.')
                else:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, f'You have successfully withdrawn ${amount}.')
                return redirect('manage_account')
        
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_username = form.cleaned_data['recipient_username']
                sender_account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(user__username=recipient_username)
                
                if amount > sender_account.balance:
                    messages.error(request, 'Insufficient funds for transfer.')
                else:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in')
                    messages.success(request, f'You have successfully transferred ${amount} to {recipient_username}.')
                return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    })
```