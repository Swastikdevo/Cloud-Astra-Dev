```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                account.balance += amount
                account.save()
                return JsonResponse({'message': 'Deposit successful!', 'new_balance': account.balance}, status=200)
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= account.balance:
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    account.balance -= amount
                    account.save()
                    return JsonResponse({'message': 'Withdrawal successful!', 'new_balance': account.balance}, status=200)
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    return render(request, 'manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```