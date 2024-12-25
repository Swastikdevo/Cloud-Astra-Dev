```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_dashboard(request):
    """View to display account details and transaction history."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_dashboard.html', {
        'account': account,
        'transactions': transactions
    })

@require_POST
@login_required
def deposit_funds(request):
    """View to handle deposits to the user's account."""
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'errors': form.errors})

@require_POST
@login_required
def withdraw_funds(request):
    """View to handle withdrawals from the user's account."""
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return JsonResponse({'success': True, 'new_balance': account.balance})
        return JsonResponse({'success': False, 'error': 'Insufficient funds.'})
    return JsonResponse({'success': False, 'errors': form.errors})
```