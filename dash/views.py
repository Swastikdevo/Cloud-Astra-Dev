```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        source_account = form.cleaned_data['source_account']
        target_account = form.cleaned_data['target_account']
        amount = form.cleaned_data['amount']
        
        if source_account.balance >= amount:
            source_account.balance -= amount
            target_account.balance += amount
            source_account.save()
            target_account.save()
            
            Transaction.objects.create(
                account=source_account,
                amount=-amount,
                transaction_type='Transfer',
                target_account=target_account
            )
            Transaction.objects.create(
                account=target_account,
                amount=amount,
                transaction_type='Transfer',
                source_account=source_account
            )
            return JsonResponse({'status': 'success', 'message': 'Transfer successful!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})

@login_required
@require_POST
def deposit_funds(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        
        account.balance += amount
        account.save()

        Transaction.objects.create(
            account=account,
            amount=amount,
            transaction_type='Deposit'
        )
        return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})

@login_required
@require_POST
def withdraw_funds(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']
        
        if account.balance >= amount:
            account.balance -= amount
            account.save()

            Transaction.objects.create(
                account=account,
                amount=-amount,
                transaction_type='Withdrawal'
            )
            return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
```