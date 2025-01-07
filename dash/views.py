```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
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
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm()

    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})

@login_required
def view_transactions(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    return render(request, 'bank/view_transactions.html', {'transactions': transactions, 'account': account})
```