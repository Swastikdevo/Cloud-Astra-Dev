```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@login_required
@csrf_exempt
def deposit_money(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'message': 'Deposit successful!', 'new_balance': account.balance})
    else:
        form = DepositForm()
    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
@csrf_exempt
def withdraw_money(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == "POST":
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            return JsonResponse({'message': 'Withdrawal successful!', 'new_balance': account.balance})
    else:
        form = WithdrawalForm()
    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transactions.html', {'transactions': transactions, 'account': account})
```