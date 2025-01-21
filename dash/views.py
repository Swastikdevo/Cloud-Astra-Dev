```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@csrf_exempt
def bank_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank_management.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        account_id = request.POST.get('account_id')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'balance': account.balance})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=account_id, user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return JsonResponse({'status': 'success', 'balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid action or form.'})
```