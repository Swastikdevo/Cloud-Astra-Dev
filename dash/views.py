```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_overview')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('account_overview')
                else:
                    error = "Insufficient funds."
                    return render(request, 'bank/account_overview.html', {'account': account, 'transactions': transactions, 'error': error})

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()

    return render(request, 'bank/account_overview.html', {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })

@csrf_exempt
@login_required
def transaction_history_api(request):
    if request.method == 'GET':
        account = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account).values('date', 'amount', 'transaction_type')
        return JsonResponse(list(transactions), safe=False)
```