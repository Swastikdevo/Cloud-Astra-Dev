```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@csrf_exempt
def account_management(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'new_balance': user_account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdraw')
                    return JsonResponse({'success': True, 'new_balance': user_account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient funds'})

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
    
    return render(request, 'account_management.html', {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```