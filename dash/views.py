```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(['GET', 'POST'])
def manage_account(request):
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)

        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'account_balance': Account.objects.get(user=request.user).balance
    })
```