```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, AccountForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST, instance=account)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('account_overview')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST, instance=account)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                    return redirect('account_overview')
                else:
                    messages.error(request, 'Insufficient funds!')
        else:
            form = AccountForm(instance=account)
    
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    return render(request, 'bank/account_overview.html', {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```