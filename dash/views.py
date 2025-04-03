```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
@csrf_exempt
def deposit_funds(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, 'Deposit successful!')
            return redirect('account_dashboard')
    else:
        form = DepositForm()

    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
@csrf_exempt
def withdraw_funds(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == "POST":
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount > account.balance:
                messages.error(request, 'Insufficient funds!')
            else:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                messages.success(request, 'Withdrawal successful!')
                return redirect('account_dashboard')
    else:
        form = WithdrawalForm()

    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})

@login_required
def transactions_view(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transactions.html', {'transactions': transactions, 'account': account})
```