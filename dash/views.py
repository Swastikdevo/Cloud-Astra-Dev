```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
def manage_accounts(request):
    if request.method == 'POST':
        # Create a new account
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return JsonResponse({'success': True, 'account_id': account.id})
        return JsonResponse({'success': False, 'errors': form.errors})

    accounts = Account.objects.all()
    return render(request, 'bank/manage_accounts.html', {'accounts': accounts})

@csrf_exempt
def deposit(request, account_id):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account_id = account_id
            transaction.type = 'deposit'
            transaction.save()
            return JsonResponse({'success': True, 'balance': transaction.account.balance})
        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'bank/deposit.html', {'account_id': account_id})

@csrf_exempt
def withdraw(request, account_id):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account_id = account_id
            transaction.type = 'withdraw'
            if transaction.amount <= transaction.account.balance:
                transaction.save()
                return JsonResponse({'success': True, 'balance': transaction.account.balance})
            return JsonResponse({'success': False, 'message': 'Insufficient funds'})
        return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'bank/withdraw.html', {'account_id': account_id})
```