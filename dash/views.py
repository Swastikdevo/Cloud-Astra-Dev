```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Account
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    """View to create or update a bank account with transaction options."""
    if account_id:
        account = get_object_or_404(Account, id=account_id)
    else:
        account = None

    if request.method == 'POST':
        if account:
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)
        
        if form.is_valid():
            account = form.save()
            messages.success(request, 'Account saved successfully!')
            return redirect('manage_account', account_id=account.id)

    else:
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form, 'account': account})

@require_http_methods(["GET", "POST"])
def transaction(request, account_id):
    """View to handle transactions such as deposits or withdrawals."""
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction_type = form.cleaned_data['transaction_type']
            amount = form.cleaned_data['amount']
            if transaction_type == 'deposit':
                account.balance += amount
                messages.success(request, f'Deposit of ${amount} successful!')
            elif transaction_type == 'withdraw' and account.balance >= amount:
                account.balance -= amount
                messages.success(request, f'Withdrawal of ${amount} successful!')
            else:
                messages.error(request, 'Insufficient funds for withdrawal.')
            account.save()
            return redirect('transaction', account_id=account.id)
    else:
        form = TransactionForm()

    return render(request, 'bank/transaction.html', {'form': form, 'account': account})
```