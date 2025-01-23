```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_dashboard(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    balance = account.balance

    return render(request, 'bank/account_dashboard.html', {
        'account': account,
        'transactions': transactions,
        'balance': balance,
    })

@login_required