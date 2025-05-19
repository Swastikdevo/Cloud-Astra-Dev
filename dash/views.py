```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@login_required
def dashboard_view(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]  # Recent transactions

    return render(request, 'bank/dashboard.html', {
        'accounts': accounts,
        'transactions': transactions,
    })

@login_required
def create_account_view(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('dashboard')
    else:
        form = AccountForm()

    return render(request, 'bank/create_account.html', {'form': form})

@login_required
@require_POST
def create_transaction_view(request):
    data = json.loads(request.body)
    form = TransactionForm(data)
    
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def view_account_details(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    return render(request, 'bank/account_detail.html', {
        'account': account,
        'transactions': transactions,
    })
```