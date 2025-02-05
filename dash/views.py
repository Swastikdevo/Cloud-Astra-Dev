```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'new_balance': account.balance})
        
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return JsonResponse({'success': True, 'new_balance': account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient balance'})
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
    
    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```