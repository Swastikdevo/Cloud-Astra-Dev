```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
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
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        return JsonResponse({'success': True, 'new_balance': account.balance})
    return JsonResponse({'success': False, 'errors': form.errors})

@require_POST
@login_required
def withdraw(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account = Account.objects.get(user=request.user)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
            return JsonResponse({'success': True, 'new_balance': account.balance})
        return JsonResponse({'success': False, 'error': 'Insufficient funds.'})
    return JsonResponse({'success': False, 'errors': form.errors})

@require_POST
@login_required
def transfer(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        recipient_username = form.cleaned_data['recipient']
        sender_account = Account.objects.get(user=request.user)
        recipient_account = Account.objects.get(user__username=recipient_username)

        if sender_account.balance >= amount:
            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()
            Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer', recipient=sender_account)
            return JsonResponse({'success': True, 'new_balance': sender_account.balance})
        return JsonResponse({'success': False, 'error': 'Insufficient funds for transfer.'})
    return JsonResponse({'success': False, 'errors': form.errors})
```