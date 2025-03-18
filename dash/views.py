```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def deposit(request, account_id):
    account = Account.objects.get(pk=account_id)
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'message': 'Deposit successful', 'new_balance': account.balance})
    return JsonResponse({'error': 'Invalid deposit amount'}, status=400)

@login_required
@require_POST
def withdraw(request, account_id):
    account = Account.objects.get(pk=account_id)
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount > account.balance:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
        return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})
    return JsonResponse({'error': 'Invalid withdrawal amount'}, status=400)

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        from_account = Account.objects.get(pk=form.cleaned_data['from_account'])
        to_account = Account.objects.get(pk=form.cleaned_data['to_account'])
        amount = form.cleaned_data['amount']
        
        if amount > from_account.balance:
            return JsonResponse({'error': 'Insufficient funds'}, status=400)
        
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()
        
        Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
        Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
        return JsonResponse({'message': 'Transfer successful', 'new_balance': from_account.balance})
    
    return JsonResponse({'error': 'Invalid transfer details'}, status=400)
```