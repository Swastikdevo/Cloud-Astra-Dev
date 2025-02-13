```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_GET
def account_summary(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'account_summary.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
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

@login_required
@require_POST
def withdraw(request):
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if amount <= account.balance:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            return JsonResponse({'success': True, 'new_balance': account.balance})
        return JsonResponse({'success': False, 'errors': {'amount': 'Insufficient funds'}})
    return JsonResponse({'success': False, 'errors': form.errors})

@login_required
@require_POST
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        recipient_account_number = form.cleaned_data['recipient_account_number']
        sender_account = Account.objects.get(user=request.user)
        recipient_account = Account.objects.get(account_number=recipient_account_number)

        if amount <= sender_account.balance:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()
            Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
            return JsonResponse({'success': True, 'new_sender_balance': sender_account.balance, 'new_recipient_balance': recipient_account.balance})
        return JsonResponse({'success': False, 'errors': {'amount': 'Insufficient funds'}})
    return JsonResponse({'success': False, 'errors': form.errors})
```