```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_management(request):
    user = request.user
    accounts = Account.objects.filter(user=user)

    if request.method == 'POST':
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                account = account_form.save(commit=False)
                account.user = user
                account.save()
                messages.success(request, 'New account created successfully!')
                return redirect('account_management')
        elif 'make_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.user = user
                transaction.save()
                messages.success(request, 'Transaction completed successfully!')
                return redirect('account_management')
    
    account_form = AccountForm()
    transaction_form = TransactionForm()

    return render(request, 'bank/account_management.html', {
        'accounts': accounts,
        'account_form': account_form,
        'transaction_form': transaction_form,
    })

@login_required
def account_details(request, account_id):
    user = request.user
    account = Account.objects.get(id=account_id, user=user)
    
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            account.delete()
            messages.success(request, 'Account deleted successfully!')
            return redirect('account_management')

    transactions = Transaction.objects.filter(account=account)

    return render(request, 'bank/account_details.html', {
        'account': account,
        'transactions': transactions,
    })
```