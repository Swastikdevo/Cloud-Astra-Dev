```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = form.cleaned_data['account']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid input.'})

@login_required
@require_POST
def withdraw(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = form.cleaned_data['account']
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
            return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'})
        return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid input.'})

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        from_account = form.cleaned_data['from_account']
        to_account = form.cleaned_data['to_account']
        amount = form.cleaned_data['amount']
        if from_account.balance >= amount:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, amount=-amount, transaction_type='Transfer')
            Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer')
            return JsonResponse({'status': 'success', 'message': 'Transfer successful.'})
        return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid input.'})
```