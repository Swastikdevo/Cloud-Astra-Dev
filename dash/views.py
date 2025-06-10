```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm
from django.db import transaction

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                with transaction.atomic():
                    account.balance += amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, type='deposit')
                return redirect('manage_account')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    with transaction.atomic():
                        account.balance -= amount
                        account.save()
                        Transaction.objects.create(account=account, amount=amount, type='withdrawal')
                    return redirect('manage_account')
                else:
                    form.add_error('amount', 'Insufficient funds.')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    }
    
    return render(request, 'bank/manage_account.html', context)
```