```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                # Handling fund transfer logic
                recipient_account = form.cleaned_data['recipient_account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer', sender=account)
                    messages.success(request, 'Transfer completed successfully!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('account_dashboard')

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit completed successfully!')
                return redirect('account_dashboard')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal completed successfully!')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('account_dashboard')

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'account': account,
        'transactions': transactions,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    
    return render(request, 'bank/account_dashboard.html', context)
```