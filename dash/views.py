```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@require_GET
def account_summary(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_summary.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def withdraw(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            return JsonResponse({'success': True, 'new_balance': account.balance})
        return JsonResponse({'success': False, 'error': 'Insufficient funds'})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        recipient_username = form.cleaned_data['recipient_username']
        amount = form.cleaned_data['amount']
        sender_account = Account.objects.get(user=request.user)
        recipient_account = Account.objects.get(user__username=recipient_username)
        
        if sender_account.balance >= amount:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()
            Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer_out')
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in')
            return JsonResponse({'success': True, 'new_balance': sender_account.balance})
        return JsonResponse({'success': False, 'error': 'Insufficient funds'})
    return JsonResponse({'success': False, 'errors': form.errors})
```