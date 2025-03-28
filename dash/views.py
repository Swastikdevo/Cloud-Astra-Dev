```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import BankAccount
from .forms import DepositForm, WithdrawForm

@login_required
@csrf_exempt
def manage_account(request):
    account = BankAccount.objects.get(user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Handling deposit
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})
        
        # Handling withdrawal
        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    return JsonResponse({'status': 'success', 'new_balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})

    # For GET request, render the account management page
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    return render(request, 'bank/manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```