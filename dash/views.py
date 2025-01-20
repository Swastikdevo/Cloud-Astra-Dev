```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_accounts(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully.'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    accounts = Account.objects.all()
    return render(request, 'bank/manage_accounts.html', {'accounts': accounts})

@csrf_exempt
@require_http_methods(["POST"])
def create_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=201)
    return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

@require_http_methods(["GET"])
def account_details(request, account_id):
    try:
        account = Account.objects.get(pk=account_id)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'bank/account_details.html', {'account': account, 'transactions': transactions})
    except Account.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Account not found.'}, status=404)

@require_http_methods(["GET"])
def transaction_history(request, account_id):
    try:
        account = Account.objects.get(pk=account_id)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'bank/transaction_history.html', {'transactions': transactions})
    except Account.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Account not found.'}, status=404)
```