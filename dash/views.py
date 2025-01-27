```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@csrf_exempt
def account_management(request):
    account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    return JsonResponse({'status': 'success', 'new_balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    return render(request, 'account_management.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```