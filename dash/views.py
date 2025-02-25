```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransactionForm
from django.contrib import messages

@login_required
def account_summary(request):
    # Fetch user's accounts
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_summary.html', {'accounts': accounts})

@login_required
def deposit_funds(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, 'Deposit successful!')
            return redirect('account_summary')
    else:
        form = TransactionForm()

    return render(request, 'bank/deposit_funds.html', {'form': form, 'account': account})

@login_required
def withdraw_funds(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                messages.success(request, 'Withdrawal successful!')
                return redirect('account_summary')
            else:
                messages.error(request, 'Insufficient funds.')
    else:
        form = TransactionForm()

    return render(request, 'bank/withdraw_funds.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

@login_required
def transfer_funds(request, from_account_id):
    from_account = Account.objects.get(id=from_account_id, user=request.user)
    if request.method == 'POST':
        to_account_id = request.POST.get('to_account_id')
        amount = float(request.POST.get('amount'))
        to_account = Account.objects.get(id=to_account_id)
        
        if amount <= from_account.balance:
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, amount=amount, transaction_type='transfer_out')
            Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer_in')
            messages.success(request, 'Transfer successful!')
            return redirect('account_summary')
        else:
            messages.error(request, 'Insufficient funds for transfer.')
    
    accounts = Account.objects.exclude(id=from_account.id).filter(user=request.user)
    return render(request, 'bank/transfer_funds.html', {'from_account': from_account, 'accounts': accounts})
```