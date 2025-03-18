```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def manage_account(request):
    account = get_object_or_404(Account, user=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return redirect('manage_account')
                else:
                    return HttpResponse("Insufficient funds.")
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    }

    return render(request, 'bank/manage_account.html', context)
```