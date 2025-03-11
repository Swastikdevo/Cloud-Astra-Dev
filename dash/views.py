```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def manage_account(request):
    # Handle deposit
    if request.method == 'POST' and 'deposit' in request.POST:
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return JsonResponse({'status': 'success', 'balance': account.balance})

    # Handle withdrawal
    elif request.method == 'POST' and 'withdraw' in request.POST:
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return JsonResponse({'status': 'success', 'balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    # Display account details and forms
    account = Account.objects.get(user=request.user)
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    return render(request, 'manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```