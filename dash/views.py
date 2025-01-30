```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    recent_transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')[:5]

    context = {
        'user_accounts': user_accounts,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'bank/dashboard.html', context)

@login_required
def deposit(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()

            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, 'Deposit successful!')
            return redirect('bank_dashboard')
    else:
        form = DepositForm()

    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdrawal(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                messages.error(request, 'Insufficient funds for this withdrawal.')
            else:
                account.balance -= amount
                account.save()

                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                messages.success(request, 'Withdrawal successful!')
                return redirect('bank_dashboard')
    else:
        form = WithdrawalForm()

    return render(request, 'bank/withdrawal.html', {'form': form, 'account': account})
```