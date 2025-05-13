```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.contrib import messages
from django.db import transaction

@login_required
def banking_dashboard(request):
    user_account = Account.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                with transaction.atomic():
                    user_account.balance += amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('banking_dashboard')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount > user_account.balance:
                    messages.error(request, 'Insufficient funds!')
                else:
                    with transaction.atomic():
                        user_account.balance -= amount
                        user_account.save()
                        Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                    return redirect('banking_dashboard')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
    
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')[:10]

    context = {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    }
    return render(request, 'banking/dashboard.html', context)
```