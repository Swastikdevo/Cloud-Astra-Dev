```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('account_list')  # Redirect to the account list

    else:
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(instance=account)
        else:
            form = AccountForm()

    return render(request, 'manage_account.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def record_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'success': True, 'transaction_id': transaction.id})

    else:
        form = TransactionForm()

    return render(request, 'record_transaction.html', {'form': form})

@login_required
def account_balance(request, account_id):
    account = Account.objects.get(id=account_id)
    balance = account.get_balance()  # Assuming this method exists in the Account model
    return JsonResponse({'account_id': account.id, 'balance': balance})
```