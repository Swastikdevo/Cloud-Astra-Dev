```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    balance = account.balance

    return render(request, 'bank/account_overview.html', {
        'account': account,
        'transactions': transactions,
        'balance': balance,
    })

@require_POST
@login_required
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = Account.objects.get(user=request.user)
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()

        # Log the transaction
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        
        return JsonResponse({'success': True, 'new_balance': account.balance}, status=200)
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@require_POST
@login_required
def withdraw(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        account = Account.objects.get(user=request.user)
        amount = form.cleaned_data['amount']

        if account.balance >= amount:
            account.balance -= amount
            account.save()

            # Log the transaction
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')

            return JsonResponse({'success': True, 'new_balance': account.balance}, status=200}
        else:
            return JsonResponse({'success': False, 'error': 'Insufficient funds'}, status=400)
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'bank/transaction_history.html', {
        'transactions': transactions,
    })
```