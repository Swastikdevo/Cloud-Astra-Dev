```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    account = None
    if account_id:
        account = get_object_or_404(Account, id=account_id)

    if request.method == "POST":
        if account:
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form, 'account': account})


@login_required
@require_http_methods(["GET", "POST"])
def create_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    else:
        form = TransactionForm()

    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})


@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})
```