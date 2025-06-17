```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.db import transaction

@login_required
def manage_account(request):
    account = get_object_or_404(Account, user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                with transaction.atomic():
                    account.balance += amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    with transaction.atomic():
                        account.balance -= amount
                        account.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('manage_account')
                else:
                    form.add_error('amount', 'Insufficient funds.')

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    }
    
    return render(request, 'manage_account.html', context)
```