```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm


@login_required
@require_http_methods(["GET", "POST"])
def account_dashboard(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_dashboard')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
                    return redirect('account_dashboard')
                else:
                    return render(request, 'account_dashboard.html', {'account': account, 'error': 'Insufficient funds'})

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                target_account = form.cleaned_data['target_account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    target_account.balance += amount
                    account.save()
                    target_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer')
                    return redirect('account_dashboard')
                else:
                    return render(request, 'account_dashboard.html', {'account': account, 'error': 'Insufficient funds'})
    
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=account).order_by('-created_at')[:10]
    
    return render(request, 'account_dashboard.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    })
```