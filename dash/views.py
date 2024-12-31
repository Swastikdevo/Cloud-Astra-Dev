```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, "Account created successfully!")
            return redirect('account_detail', account.id)
        else:
            messages.error(request, "Error creating account. Please try again.")
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def make_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction completed successfully!")
            return redirect('transaction_history')
        else:
            messages.error(request, "Error processing transaction. Please try again.")
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/make_transaction.html', {'form': form, 'transactions': transactions})
```