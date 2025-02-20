```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    """ View to show user's account details and recent transactions. """
    user_accounts = Account.objects.filter(owner=request.user)
    recent_transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')[:5]
    return render(request, 'bank/account_overview.html', {
        'user_accounts': user_accounts,
        'recent_transactions': recent_transactions,
    })

@login_required
@require_POST
def deposit(request, account_id):
    """ View to handle deposits into a bank account. """
    account = Account.objects.get(id=account_id, owner=request.user)
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})
    return JsonResponse({'error': 'Invalid form data'}, status=400)

@login_required
@require_POST
def withdraw(request, account_id):
    """ View to handle withdrawals from a bank account. """
    account = Account.objects.get(id=account_id, owner=request.user)
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount > account.balance:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
        return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})
    return JsonResponse({'error': 'Invalid form data'}, status=400)
```