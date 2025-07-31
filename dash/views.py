```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    else:
        account = Account.objects.get(id=account_id) if account_id else None
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form})


@require_http_methods(["POST"])
def perform_transaction(request, account_id):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = Account.objects.get(id=account_id)
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=201)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_http_methods(["GET"])
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})
```