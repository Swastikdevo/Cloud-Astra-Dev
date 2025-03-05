```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@csrf_exempt
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
                return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient balance'}, status=400)

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    account = Account.objects.get(user=request.user)
    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'balance': account.balance,
    })
```