```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'balance': account.balance})
        
        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(id=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return JsonResponse({'status': 'success', 'balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

        elif action == 'view_balance':
            account = Account.objects.get(id=request.POST.get('account_id'))
            return JsonResponse({'status': 'success', 'balance': account.balance})

    return render(request, 'manage_account.html', {
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
    })
```