```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_summary(request):
    user_accounts = Account.objects.filter(owner=request.user)
    total_balance = sum(account.balance for account in user_accounts)
    
    return render(request, 'bank/account_summary.html', {
        'accounts': user_accounts,
        'total_balance': total_balance,
    })

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        new_account = form.save(commit=False)
        new_account.owner = request.user
        new_account.save()
        return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})

@login_required
@require_POST
def make_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        new_transaction = form.save(commit=False)
        new_transaction.account = form.cleaned_data['account']
        new_transaction.save()
        return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid transaction data.'})

@login_required
def transaction_history(request):
    user_transactions = Transaction.objects.filter(account__owner=request.user).order_by('-date')
    
    return render(request, 'bank/transaction_history.html', {
        'transactions': user_transactions,
    })
```