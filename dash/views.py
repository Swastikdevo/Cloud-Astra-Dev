```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    total_balance = sum(account.balance for account in accounts)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts, 'total_balance': total_balance})

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        new_account = form.save(commit=False)
        new_account.user = request.user
        new_account.save()
        messages.success(request, 'Account created successfully!')
        return redirect('account_dashboard')
    else:
        messages.error(request, 'Error creating account. Please check the form.')
        return render(request, 'bank/create_account.html', {'form': form})

@login_required
@require_POST
def deposit(request, account_id):
    amount = request.POST.get('amount')
    try:
        amount = float(amount)
        account = Account.objects.get(id=account_id, user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        messages.success(request, 'Deposit successful!')
    except (ValueError, Account.DoesNotExist):
        messages.error(request, 'Invalid deposit amount or account.')
    return redirect('account_dashboard')

@login_required
@require_POST
def withdraw(request, account_id):
    amount = request.POST.get('amount')
    try:
        amount = float(amount)
        account = Account.objects.get(id=account_id, user=request.user)
        if amount > account.balance:
            messages.error(request, 'Insufficient funds.')
        else:
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
            messages.success(request, 'Withdrawal successful!')
    except (ValueError, Account.DoesNotExist):
        messages.error(request, 'Invalid withdrawal amount or account.')
    return redirect('account_dashboard')

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})
```