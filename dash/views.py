```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if account_id:
        account = Account.objects.get(pk=account_id)
    else:
        account = None

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_list')
    else:
        form = AccountForm(instance=account)

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'manage_account.html', context)

@require_http_methods(["GET", "POST"])
def perform_transaction(request, account_id):
    account = Account.objects.get(pk=account_id)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        form = TransactionForm()

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'perform_transaction.html', context)

@require_http_methods(["GET"])
def transaction_history(request, account_id):
    account = Account.objects.get(pk=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'transaction_history.html', context)
```