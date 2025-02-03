```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=Account.objects.get(id=account_id) if account_id else None)
        if form.is_valid():
            account = form.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm(instance=Account.objects.get(id=account_id) if account_id else None)

    return render(request, 'manage_account.html', {'form': form})

@require_http_methods(["POST"])
def create_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@require_http_methods(["GET"])
def account_balance(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        balance = account.get_balance()
        return JsonResponse({'account_id': account.id, 'balance': balance})
    except Account.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Account not found'}, status=404)
```