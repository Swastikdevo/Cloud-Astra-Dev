```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import BankAccount, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def bank_dashboard(request):
    accounts = BankAccount.objects.filter(user=request.user)
    context = {
        'accounts': accounts,
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
    }
    return render(request, 'bank/dashboard.html', context)

@login_required
@require_POST
def deposit_funds(request, account_id):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = BankAccount.objects.get(id=account_id, user=request.user)
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def withdraw_funds(request, account_id):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        account = BankAccount.objects.get(id=account_id, user=request.user)
        amount = form.cleaned_data['amount']
        if amount > account.balance:
            return JsonResponse({'success': False, 'errors': 'Insufficient funds'})
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
        return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'errors': form.errors})
```