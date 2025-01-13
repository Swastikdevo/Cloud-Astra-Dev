```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            messages.success(request, "Account created successfully!")
            return redirect('manage_account')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})


@login_required
@require_http_methods(["GET", "POST"])
def transfer_funds(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.sender = request.user
            transaction.save()
            messages.success(request, "Transfer successful!")
            return redirect('transfer_funds')
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(sender=request.user)
    return render(request, 'bank/transfer_funds.html', {'form': form, 'transactions': transactions})


@login_required
@require_http_methods(["GET"])
def account_summary(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(sender=request.user, account=account)
    return render(request, 'bank/account_summary.html', {'account': account, 'transactions': transactions})


@login_required
@require_http_methods(["POST"])
def delete_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        account.delete()
        messages.success(request, "Account deleted successfully!")
    except Account.DoesNotExist:
        messages.error(request, "Account not found!")
    return redirect('manage_account')
```