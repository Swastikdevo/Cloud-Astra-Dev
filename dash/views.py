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
    user_account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='deposit')
                return JsonResponse({'message': f'Deposited ${amount} successfully!', 'new_balance': user_account.balance})
        
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='withdraw')
                    return JsonResponse({'message': f'Withdrew ${amount} successfully!', 'new_balance': user_account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    return render(request, 'manage_account.html', {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```