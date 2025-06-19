```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:  # Update existing account
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Account updated successfully!'})
        else:  # Create new account
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})

    # Fetch the account if it exists
    account = Account.objects.get(id=account_id) if account_id else None
    form = AccountForm(instance=account)
    
    return render(request, 'bank/manage_account.html', {'form': form})

@require_http_methods(["GET", "POST"])
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction created successfully!', 'transaction_id': transaction.id})
    
    form = TransactionForm()
    return render(request, 'bank/create_transaction.html', {'form': form})

@require_http_methods(["GET"])
def view_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        return render(request, 'bank/view_transaction.html', {'transaction': transaction})
    except Transaction.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Transaction not found!'}, status=404)
```