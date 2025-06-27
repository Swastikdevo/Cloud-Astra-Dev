```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def bank_dashboard(request):
    """Render the bank dashboard with account summary and latest transactions."""
    user_accounts = Account.objects.filter(owner=request.user)
    latest_transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')[:5]
    
    context = {
        'accounts': user_accounts,
        'latest_transactions': latest_transactions,
    }
    
    return render(request, 'bank/dashboard.html', context)

@login_required
def create_account(request):
    """Create a new bank account for the user."""
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return redirect('bank:dashboard')
    else:
        form = AccountForm()
    
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def view_account(request, account_id):
    """View details of a specific account."""
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    
    return render(request, 'bank/view_account.html', context)

@login_required
def make_transaction(request, account_id):
    """Handle fund transfer and deposit/withdrawal requests."""
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction completed'})
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})
```