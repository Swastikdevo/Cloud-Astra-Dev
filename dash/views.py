```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'manage_account.html', context)
```