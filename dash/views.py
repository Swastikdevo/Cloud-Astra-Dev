```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_overview(request):
    account = get_object_or_404(Account, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdrawal_form': WithdrawalForm(),
        'transfer_form': TransferForm(),
    }
    return render(request, 'bank/account_overview.html', context)

@require_POST
@login_required
def deposit(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = get_object_or_404(Account, owner=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@require_POST
@login_required
def withdraw(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = get_object_or_404(Account, owner=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@require_POST
@login_required
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        recipient_username = form.cleaned_data['recipient']
        sender_account = get_object_or_404(Account, owner=request.user)
        recipient_account = get_object_or_404(Account, owner__username=recipient_username)
        
        if sender_account.balance >= amount:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()
            Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer_out')
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in')
            return JsonResponse({'status': 'success', 'new_sender_balance': sender_account.balance, 'new_recipient_balance': recipient_account.balance})
        return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    return JsonResponse({'status': 'error', 'errors': form.errors})
```