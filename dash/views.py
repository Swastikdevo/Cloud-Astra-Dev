```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'account_id': account.id})
        return JsonResponse({'status': 'failure', 'errors': form.errors})

    accounts = Account.objects.filter(user=request.user)
    form = AccountForm()
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def make_transaction(request, account_id):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=account_id, user=request.user)
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        return JsonResponse({'status': 'failure', 'errors': form.errors})

    account = Account.objects.get(id=account_id, user=request.user)
    form = TransactionForm()
    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    transactions = Transaction.objects.filter(account__id=account_id, account__user=request.user)
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```