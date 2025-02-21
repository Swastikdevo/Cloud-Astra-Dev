```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('account_overview')
    else:
        form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def deposit_funds(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount and amount.isdigit() and int(amount) > 0:
            account.balance += int(amount)
            account.save()
            Transaction.objects.create(account=account, amount=int(amount), transaction_type='deposit')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Invalid amount'})
    return render(request, 'bank/deposit_funds.html', {'account': account})

@login_required
def withdraw_funds(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount and amount.isdigit() and int(amount) > 0 and account.balance >= int(amount):
            account.balance -= int(amount)
            account.save()
            Transaction.objects.create(account=account, amount=int(amount), transaction_type='withdraw')
            return JsonResponse({'status': 'success', 'new_balance': account.balance})
        return JsonResponse({'status': 'error', 'message': 'Invalid withdrawal'})
    return render(request, 'bank/withdraw_funds.html', {'account': account})

@login_required
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})
```