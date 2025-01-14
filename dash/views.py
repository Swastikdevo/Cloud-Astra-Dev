```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
import json

@login_required
@csrf_exempt
def account_dashboard(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

    elif request.method == 'POST':
        data = json.loads(request.body)
        if data.get("action") == "deposit":
            return handle_deposit(request, data)
        elif data.get("action") == "withdraw":
            return handle_withdraw(request, data)
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

def handle_deposit(request, data):
    form = DepositForm(data)
    if form.is_valid():
        account = Account.objects.get(id=data.get('account_id'), user=request.user)
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        messages.success(request, 'Deposit successful!')
        return JsonResponse({'msg': 'Deposit successful!'}, status=200)
    else:
        return JsonResponse({'error': form.errors}, status=400)

def handle_withdraw(request, data):
    form = WithdrawForm(data)
    if form.is_valid():
        account = Account.objects.get(id=data.get('account_id'), user=request.user)
        amount = form.cleaned_data['amount']
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
            messages.success(request, 'Withdrawal successful!')
            return JsonResponse({'msg': 'Withdrawal successful!'}, status=200)
        else:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
    else:
        return JsonResponse({'error': form.errors}, status=400)
```