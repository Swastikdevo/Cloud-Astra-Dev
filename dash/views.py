```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        # Handle deposit
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})

        # Handle withdrawal
        withdraw_form = WithdrawForm(request.POST)
        if withdraw_form.is_valid():
            amount = withdraw_form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    context = {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'account_balance': Account.objects.get(user=request.user).balance,
    }
    return render(request, 'bank/manage_account.html', context)
```