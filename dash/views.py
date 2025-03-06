```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_accounts(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('manage_accounts')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_accounts.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def manage_transactions(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.account = account
            new_transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction created successfully!'})
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date_created')
    return render(request, 'bank/manage_transactions.html', {'form': form, 'transactions': transactions, 'account': account})

@login_required
@require_http_methods(["POST"])
def delete_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        account.delete()
        return JsonResponse({'status': 'success', 'message': 'Account deleted successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request!'}, status=400)
```