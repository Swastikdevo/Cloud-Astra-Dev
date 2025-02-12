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
    user_account = Account.objects.get(owner=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'balance': user_account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Withdraw')
                    return JsonResponse({'status': 'success', 'balance': user_account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    context = {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    
    return render(request, 'bank/manage_account.html', context)
```