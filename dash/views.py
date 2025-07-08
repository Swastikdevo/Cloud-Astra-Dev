```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    account = get_object_or_404(BankAccount, user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('manage_account')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient_username']
                amount = form.cleaned_data['amount']
                recipient = get_object_or_404(BankAccount, user__username=recipient_username)
                
                if amount <= account.balance:
                    account.balance -= amount
                    recipient.balance += amount
                    account.save()
                    recipient.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer to {}'.format(recipient_username))
                    Transaction.objects.create(account=recipient, amount=amount, transaction_type='Transfer from {}'.format(request.user.username))
                    return redirect('manage_account')
    
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')[:10]

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }

    return render(request, 'bank/manage_account.html', context)
```