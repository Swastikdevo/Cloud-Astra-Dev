```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                account.balance += amount
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Deposit successful'})
            else:
                return JsonResponse({'status': 'error', 'message': form.errors})

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    account.balance -= amount
                    account.save()
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
            else:
                return JsonResponse({'status': 'error', 'message': form.errors})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
```