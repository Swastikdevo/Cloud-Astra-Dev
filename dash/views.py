```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_http_methods(["GET", "POST"])
def manage_accounts(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_accounts')
    else:
        form = AccountForm()

    accounts = Account.objects.all()
    return render(request, 'bank/manage_accounts.html', {'form': form, 'accounts': accounts})

@require_http_methods(["GET", "POST"])
def record_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({'success': True, 'transaction_id': transaction.id})
    else:
        form = TransactionForm()

    return render(request, 'bank/record_transaction.html', {'form': form})

@require_http_methods(["GET"])
def account_balance(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        balance = account.get_balance()
        return JsonResponse({'account_id': account_id, 'balance': balance})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

@require_http_methods(["GET"])
def list_transactions(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'bank/list_transactions.html', {'transactions': transactions, 'account': account})
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)
```