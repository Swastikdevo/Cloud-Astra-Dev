```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_overview.html', {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
        'transfer_form': TransferForm(),
    })

@require_POST
@login_required
def deposit(request):
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
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return JsonResponse({'success': True, 'new_balance': account.balance})
        return JsonResponse({'success': False, 'error': 'Insufficient balance.'})
    return JsonResponse({'success': False, 'errors': form.errors})

@require_POST
@login_required
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        target_account_number = form.cleaned_data['target_account_number']
        account = Account.objects.get(user=request.user)
        target_account = Account.objects.filter(account_number=target_account_number).first()
        
        if target_account and account.balance >= amount:
            account.balance -= amount
            target_account.balance += amount
            account.save()
            target_account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
            return JsonResponse({'success': True, 'new_balance': account.balance})
        return JsonResponse({'success': False, 'error': 'Insufficient balance or target account not found.'})
    return JsonResponse({'success': False, 'errors': form.errors})
```