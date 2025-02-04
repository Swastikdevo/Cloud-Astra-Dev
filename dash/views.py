```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id):
    account = Account.objects.get(id=account_id)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'new_balance': account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return JsonResponse({'success': True, 'new_balance': account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient funds'})

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    return render(request, 'manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form
    })
```