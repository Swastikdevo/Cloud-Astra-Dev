```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import CreateAccountForm, TransactionForm

@login_required
def manage_accounts(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_list')
    else:
        form = CreateAccountForm()

    user_accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_accounts.html', {'form': form, 'user_accounts': user_accounts})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('transaction_history')
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'form': form})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```