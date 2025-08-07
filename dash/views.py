```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
    else:
        form = AccountForm()
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def perform_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('perform_transaction')
    else:
        form = TransactionForm()
    
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'bank/perform_transaction.html', {'form': form, 'transactions': transactions})

@login_required
def account_balance(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        balance = account.get_balance()  # Assume get_balance method exists
        return JsonResponse({'account_id': account.id, 'balance': balance})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
```