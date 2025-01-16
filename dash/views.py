```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankAccount, Transaction
from .forms import BankAccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = BankAccountForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.user = request.user
            bank_account.save()
            messages.success(request, "New bank account created successfully.")
            return redirect('manage_account')
    else:
        form = BankAccountForm()

    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def make_transaction(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, "Transaction recorded successfully.")
            return redirect('make_transaction', account_id=account.id)
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=account)
    return render(request, 'make_transaction.html', {'form': form, 'account': account, 'transactions': transactions})

@login_required
@require_http_methods(["POST"])
def delete_account(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    account.delete()
    messages.success(request, "Bank account deleted successfully.")
    return redirect('manage_account')
```