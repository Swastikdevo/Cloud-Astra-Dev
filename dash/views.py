```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_summary(request):
    """View to display account summary with balance and recent transactions."""
    accounts = Account.objects.filter(user=request.user)
    context = {
        'accounts': accounts,
    }
    return render(request, 'bank/account_summary.html', context)

@login_required
@require_POST
def create_account(request):
    """View to create a new bank account."""
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        return JsonResponse({'status': 'success', 'account_id': account.id}, status=201)
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@login_required
def account_detail(request, account_id):
    """View to display details for a specific account."""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/account_detail.html', context)

@login_required
@require_POST
def add_transaction(request, account_id):
    """View to add a new transaction to a specified account."""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=201)
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@login_required
def transaction_history(request, account_id):
    """View to retrieve transaction history for a specific account."""
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/transaction_history.html', context)
```