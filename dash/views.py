```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    """View to display account details and recent transactions."""
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
    }
    return render(request, 'account/overview.html', context)

@require_POST
@login_required
def deposit(request):
    """View to handle deposits into the user account."""
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
def withdraw(request):
    """View to handle withdrawals from the user account."""
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)

        if amount > account.balance:
            return JsonResponse({'success': False, 'message': 'Insufficient funds.'})

        account.balance -= amount
        account.save()

        Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')

        return JsonResponse({'success': True, 'new_balance': account.balance})

    return JsonResponse({'success': False, 'errors': form.errors})
```