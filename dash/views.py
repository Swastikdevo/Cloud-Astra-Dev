```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    context = {
        'accounts': user_accounts
    }
    return render(request, 'bank/account_dashboard.html', context)

@login_required
@require_POST
def deposit(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    form = DepositForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_POST
def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    form = WithdrawForm(request.POST)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        if amount > account.balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
        return JsonResponse({'status': 'success', 'new_balance': account.balance})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
@require_POST
def transfer(request, from_account_id):
    from_account = get_object_or_404(Account, id=from_account_id, owner=request.user)
    form = TransferForm(request.POST)
    if form.is_valid():
        to_account_id = form.cleaned_data['to_account_id']
        amount = form.cleaned_data['amount']
        to_account = get_object_or_404(Account, id=to_account_id)

        if amount > from_account.balance:
            return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
        
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()
        
        Transaction.objects.create(account=from_account, amount=amount, transaction_type='transfer-out')
        Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer-in')
        return JsonResponse({'status': 'success', 'new_from_balance': from_account.balance, 'new_to_balance': to_account.balance})

    return JsonResponse({'status': 'error', 'errors': form.errors})
```