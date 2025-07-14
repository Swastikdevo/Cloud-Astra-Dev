```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': user_accounts})

@login_required
def perform_transaction(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']

            if transaction_type == 'deposit':
                account.balance += amount
                messages.success(request, 'Deposit successful!')
            elif transaction_type == 'withdrawal':
                if account.balance >= amount:
                    account.balance -= amount
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                    return redirect('account_overview')

            account.save()

            # Log the transaction
            transaction = Transaction(account=account, amount=amount, transaction_type=transaction_type)
            transaction.save()

            return redirect('account_overview')
    else:
        form = TransactionForm()

    return render(request, 'bank/transaction_form.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    transactions = Transaction.objects.filter(account__id=account_id)
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

@login_required
def account_balance_api(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    return JsonResponse({'balance': account.balance})
```