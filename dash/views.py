```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_dashboard')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('account_dashboard')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form
    }
    return render(request, 'bank/account_dashboard.html', context)

@login_required
def recent_transactions(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]
    transaction_data = [{"date": txn.date, "amount": txn.amount, "type": txn.transaction_type} for txn in transactions]
    return JsonResponse(transaction_data, safe=False)
```