```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def manage_account(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('manage_account')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions
    })
```