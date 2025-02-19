```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Withdrawal')
                    return redirect('manage_account')
                else:
                    return render(request, 'account/manage_account.html', {'error': 'Insufficient funds!', 'account': user_account, 'deposit_form': DepositForm(), 'withdraw_form': WithdrawalForm()})
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawalForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    return render(request, 'account/manage_account.html', {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    })

@login_required
def transaction_history(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    return render(request, 'account/transaction_history.html', {
        'transactions': transactions,
        'account': user_account,
    })

@login_required
def account_balance(request):
    user_account = Account.objects.get(user=request.user)
    return JsonResponse({'balance': user_account.balance})
```