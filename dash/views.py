```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    """View to manage a user's bank account."""
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=user_account)
        if form.is_valid():
            form.save()
            return redirect('account_summary')
    else:
        form = AccountForm(instance=user_account)

    return render(request, 'manage_account.html', {'form': form, 'account': user_account})

@login_required
def transaction_history(request):
    """View to display transaction history for a user's account."""
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    return render(request, 'transaction_history.html', {'transactions': transactions})

@login_required
def create_transaction(request):
    """View to create a new transaction."""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.account = Account.objects.get(user=request.user)
            new_transaction.save()
            return redirect('transaction_history')
    else:
        form = TransactionForm()

    return render(request, 'create_transaction.html', {'form': form})

@login_required
def account_summary(request):
    """View to display a summary of the user's account."""
    user_account = Account.objects.get(user=request.user)
    balance = user_account.balance

    return render(request, 'account_summary.html', {'account': user_account, 'balance': balance})
```