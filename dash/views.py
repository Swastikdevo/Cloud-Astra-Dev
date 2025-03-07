```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if request.method == "POST":
        # Handle account creation or update
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Account saved!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    
    if account_id:
        account = get_object_or_404(Account, id=account_id, user=request.user)
        form = AccountForm(instance=account)
    else:
        form = AccountForm()

    return render(request, 'manage_account.html', {'form': form})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def make_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        return JsonResponse({'status': 'success', 'message': 'Transaction completed!'})
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def account_balance(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    balance = account.balance
    return JsonResponse({'account_id': account.id, 'balance': balance})
```