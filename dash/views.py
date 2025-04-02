```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                transaction = Transaction(account=account, amount=amount, transaction_type='Deposit')
                transaction.save()
                return JsonResponse({'status': 'success', 'balance': account.balance})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    transaction = Transaction(account=account, amount=amount, transaction_type='Withdraw')
                    transaction.save()
                    return JsonResponse({'status': 'success', 'balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    return render(request, 'bank/manage_account.html', {
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
        'balance': Account.objects.get(user=request.user).balance,
    })
```