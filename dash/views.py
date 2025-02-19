```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('manage_account')
    else:
        account_form = AccountForm()
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {
        'account_form': account_form,
        'accounts': accounts,
    })

@login_required
@require_http_methods(["GET", "POST"])
def perform_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'success': True, 'message': 'Transaction successful!'})
    else:
        transaction_form = TransactionForm()
    
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'bank/perform_transaction.html', {
        'transaction_form': transaction_form,
        'transactions': transactions,
    })

@login_required
@require_http_methods(["GET"])
def account_balance(request):
    accounts = Account.objects.filter(user=request.user)
    balances = {account.id: account.balance for account in accounts}
    return JsonResponse({'balances': balances})
```