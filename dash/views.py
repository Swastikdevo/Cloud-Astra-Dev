```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                account = account_form.save(commit=False)
                account.user = request.user
                account.save()
                messages.success(request, 'Account created successfully.')
                return redirect('manage_account')
                
        elif 'make_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, 'Transaction completed successfully.')
                return redirect('manage_account')

    else:
        account_form = AccountForm()
        transaction_form = TransactionForm()

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'account_form': account_form,
        'transaction_form': transaction_form,
        'accounts': accounts,
        'transactions': transactions,
    }
    
    return render(request, 'bank/manage_account.html', context)
```