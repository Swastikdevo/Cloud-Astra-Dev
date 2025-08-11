```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.core.exceptions import ObjectDoesNotExist


@login_required
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            account = Account.objects.get(pk=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        if account_id:
            account = Account.objects.get(pk=account_id)
            form = AccountForm(instance=account)
        else:
            form = AccountForm()

    return render(request, 'manage_account.html', {'form': form, 'account_id': account_id})


@login_required
def deposit_funds(request, account_id):
    if request.method == 'POST':
        account = Account.objects.get(pk=account_id)
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = 'Deposit'
            transaction.save()
            account.balance += transaction.amount
            account.save()
            return JsonResponse({'status': 'success', 'new_balance': account.balance})

    return render(request, 'deposit_funds.html', {'account_id': account_id})


@login_required
def withdraw_funds(request, account_id):
    if request.method == 'POST':
        account = Account.objects.get(pk=account_id)
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.transaction_type = 'Withdrawal'
            if account.balance >= transaction.amount:
                transaction.save()
                account.balance -= transaction.amount
                account.save()
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    return render(request, 'withdraw_funds.html', {'account_id': account_id})


@login_required
def transfer_funds(request, account_id):
    if request.method == 'POST':
        account_from = Account.objects.get(pk=account_id)
        account_to_id = request.POST.get('account_to')
        try:
            account_to = Account.objects.get(pk=account_to_id)
            amount = float(request.POST.get('amount'))
            if account_from.balance >= amount:
                account_from.balance -= amount
                account_to.balance += amount
                account_from.save()
                account_to.save()
                return JsonResponse({'status': 'success', 'new_balance_from': account_from.balance, 'new_balance_to': account_to.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Destination account does not exist'})

    return render(request, 'transfer_funds.html', {'account_id': account_id})
```