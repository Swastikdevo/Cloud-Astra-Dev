```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    user_account = Account.objects.get(user=request.user)
    
    if request.method == "POST":
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(
                    account=user_account,
                    amount=amount,
                    transaction_type='deposit'
                )
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount > user_account.balance:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance!'})
                user_account.balance -= amount
                user_account.save()
                Transaction.objects.create(
                    account=user_account,
                    amount=amount,
                    transaction_type='withdrawal'
                )
                return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
    
    return render(request, 'manage_account.html', {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```