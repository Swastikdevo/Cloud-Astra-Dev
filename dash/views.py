```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.http import JsonResponse

@require_http_methods(["GET", "POST"])
def manage_accounts(request):
    if request.method == "POST":
        # Handle new account creation
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully.'}, status=201)
        return JsonResponse({'status': 'error', 'message': 'Failed to create account.'}, status=400)

    accounts = Account.objects.all()
    return render(request, 'manage_accounts.html', {'accounts': accounts})

@require_http_methods(["GET", "POST"])
def process_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction processed successfully.', 'transaction_id': transaction.id}, status=201)
        return JsonResponse({'status': 'error', 'message': 'Failed to process transaction.'}, status=400)

    form = TransactionForm()
    return render(request, 'process_transaction.html', {'form': form})

@require_http_methods(["GET"])
def account_details(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'account_details.html', {'account': account, 'transactions': transactions})
    except Account.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Account not found.'}, status=404)
```