```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                    return redirect('manage_account')
                else:
                    messages.error(request, 'Insufficient funds!')
                    return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions
    })
```