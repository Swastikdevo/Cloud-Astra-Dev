```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return redirect('account_details', account_id=account.id)
    else:
        form = AccountForm()

    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def perform_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=request.POST['account_id'], owner=request.user)
            transaction.save()
            # Update account balance
            transaction.account.balance += transaction.amount if transaction.transaction_type == 'deposit' else -transaction.amount
            transaction.account.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        form = TransactionForm()

    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/perform_transaction.html', {'form': form, 'accounts': accounts})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(account__owner=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```