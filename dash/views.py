```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    # Fetch the account information for the logged-in user
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('account_overview')  # Redirect to avoid re-submission

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                    return redirect('account_overview')
                else:
                    return HttpResponse("Insufficient funds.")

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    
    return render(request, 'bank/account_overview.html', context)
```