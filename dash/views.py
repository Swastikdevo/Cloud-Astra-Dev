```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    form = TransactionForm(request.POST)

    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})
```