```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(['GET', 'POST'])
def account_management(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_management')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'account_management.html', {'form': form, 'accounts': accounts})


@login_required
@require_http_methods(['GET', 'POST'])
def transaction_management(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully.'})
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transaction_management.html', {'form': form, 'transactions': transactions})

@login_required
def account_balance(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    balance = account.get_balance()
    return JsonResponse({'account_id': account_id, 'balance': balance})
```