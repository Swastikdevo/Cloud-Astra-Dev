```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
from django.contrib import messages
from django.db import transaction


@login_required
def perform_transaction(request, account_id):
    account = Account.objects.get(id=account_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        
        if form.is_valid():
            transaction_type = form.cleaned_data['transaction_type']
            amount = form.cleaned_data['amount']

            if transaction_type == 'deposit':
                account.balance += amount
                transaction = Transaction(account=account, amount=amount, transaction_type='Deposit')
            elif transaction_type == 'withdraw':
                if amount > account.balance:
                    messages.error(request, "Insufficient funds.")
                    return redirect('perform_transaction', account_id=account_id)
                account.balance -= amount
                transaction = Transaction(account=account, amount=amount, transaction_type='Withdraw')

            with transaction.atomic():
                account.save()
                transaction.save()
                messages.success(request, "Transaction successful!")
                return redirect('account_detail', account_id=account_id)
        else:
            messages.error(request, "Invalid data. Please correct the errors.")
    
    else:
        form = TransactionForm()
    
    return render(request, 'perform_transaction.html', {'form': form, 'account': account})
```