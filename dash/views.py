```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import CreateAccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        # Creating a new account
        if 'create_account' in request.POST:
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                messages.success(request, 'New account created successfully.')
                return redirect('manage_account')

        # Processing a transaction
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, 'Transaction completed successfully.')
                return redirect('manage_account')
    
    # Retrieve user accounts and transactions for display
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    create_account_form = CreateAccountForm()
    transaction_form = TransactionForm()

    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'transactions': transactions,
        'create_account_form': create_account_form,
        'transaction_form': transaction_form,
    })
```