```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm
import json

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        # Fetch account details
        account = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account).order_by('-date')
        return render(request, 'account_management.html', {'account': account, 'transactions': transactions})
    
    if request.method == 'POST':
        # Handle deposit
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('account_management')
            else:
                messages.error(request, 'Invalid deposit amount.')

        # Handle withdrawal
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                    return redirect('account_management')
                else:
                    messages.error(request, 'Insufficient funds.')
            else:
                messages.error(request, 'Invalid withdrawal amount.')
    
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
```