```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import BankAccount, Transaction
from .forms import BankAccountForm, TransactionForm

@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_bank_accounts(request):
    if request.method == "POST":
        form = BankAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    accounts = BankAccount.objects.all()
    return render(request, 'bank/manage_accounts.html', {'accounts': accounts})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def manage_transactions(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully!'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    transactions = Transaction.objects.all()
    return render(request, 'bank/manage_transactions.html', {'transactions': transactions})

def account_details(request, account_id):
    try:
        account = BankAccount.objects.get(id=account_id)
        transactions = account.transaction_set.all()
        return render(request, 'bank/account_details.html', {'account': account, 'transactions': transactions})
    except BankAccount.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Account not found!'}, status=404)
```