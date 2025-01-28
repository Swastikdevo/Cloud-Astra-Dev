```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def banking_view(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('banking')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return redirect('banking')
                else:
                    return render(request, 'banking.html', {'account': account, 'error': 'Insufficient funds!'})

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    try:
                        recipient_account = Account.objects.get(user__username=recipient_username)
                        account.balance -= amount
                        recipient_account.balance += amount
                        account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer', recipient=recipient_username)
                        return redirect('banking')
                    except Account.DoesNotExist:
                        return render(request, 'banking.html', {'account': account, 'error': 'Recipient not found!'})
                else:
                    return render(request, 'banking.html', {'account': account, 'error': 'Insufficient funds!'})

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()
    
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'banking.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions
    })
```