```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = request.user.account
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.', 'new_balance': account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = request.user.account
                if amount > account.balance:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'}, status=400)
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.', 'new_balance': account.balance})

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    return render(request, 'account/manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'balance': request.user.account.balance,
    })
```