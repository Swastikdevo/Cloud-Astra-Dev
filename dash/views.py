```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        # Fetch all accounts for the logged-in user
        accounts = Account.objects.filter(user=request.user)
        form = AccountForm()
        return render(request, 'bank/account_management.html', {'accounts': accounts, 'form': form})
    
    elif request.method == 'POST':
        # Handle account creation
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully.')
            return redirect('account_management')
        else:
            messages.error(request, 'Failed to create account. Please correct the errors below.')
        
        return render(request, 'bank/account_management.html', {'form': form})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

@login_required
@csrf_exempt
def perform_transaction(request, account_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        transaction_type = data.get('transaction_type')  # 'deposit' or 'withdraw'

        account = Account.objects.get(id=account_id, user=request.user)

        if transaction_type == 'deposit':
            account.balance += amount
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
        elif transaction_type == 'withdraw':
            if account.balance >= amount:
                account.balance -= amount
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
            else:
                return JsonResponse({'error': 'Insufficient funds.'}, status=400)

        account.save()
        return JsonResponse({'message': 'Transaction completed successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
```