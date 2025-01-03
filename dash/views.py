```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('manage_account')
                else:
                    return JsonResponse({'error': 'Insufficient balance'}, status=400)

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        account = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'bank/manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'account': account,
        'transactions': transactions
    })
```