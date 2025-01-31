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
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account_management.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                
                account.balance += amount
                account.save()
                
                transaction = Transaction(account=account, amount=amount, transaction_type='Deposit')
                transaction.save()

                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']

                if account.balance >= amount:
                    account.balance -= amount
                    account.save()

                    transaction = Transaction(account=account, amount=amount, transaction_type='Withdraw')
                    transaction.save()

                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
```