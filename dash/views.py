```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.db import transaction

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm()

    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
def create_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        with transaction.atomic():
            transaction_instance = form.save(commit=False)
            transaction_instance.user = request.user
            transaction_instance.save()
            # Update account balance
            account = transaction_instance.account
            if transaction_instance.transaction_type == 'credit':
                account.balance += transaction_instance.amount
            elif transaction_instance.transaction_type == 'debit':
                account.balance -= transaction_instance.amount
            account.save()
        return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid transaction data.'})

@login_required
@require_http_methods(["GET"])
def account_details(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/account_details.html', {'account': account, 'transactions': transactions})
```