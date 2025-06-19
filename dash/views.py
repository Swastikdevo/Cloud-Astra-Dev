```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    """View to display account details and recent transactions."""
    account = Account.objects.get(user=request.user)
    recent_transactions = Transaction.objects.filter(account=account).order_by('-date')[:5]

    return render(request, 'bank/account_overview.html', {
        'account': account,
        'recent_transactions': recent_transactions,
    })

@login_required
@require_POST
def deposit_funds(request):
    """View to handle deposits to the user's account."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')

        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_POST
def withdraw_funds(request):
    """View to handle withdrawals from the user's account."""
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)

        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')

            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})
```