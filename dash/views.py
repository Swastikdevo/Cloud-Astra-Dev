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
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {
        'account_form': account_form,
        'accounts': accounts
    })

@login_required
@require_http_methods(["GET", "POST"])
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user)
    return render(request, 'bank/transaction_history.html', {
        'transactions': transactions
    })

@login_required
@require_http_methods(["POST"])
def create_transaction(request):
    transaction_form = TransactionForm(request.POST)
    if transaction_form.is_valid():
        transaction = transaction_form.save(commit=False)
        transaction.account = Account.objects.get(id=request.POST.get('account_id'), user=request.user)
        transaction.save()
        return JsonResponse({'message': 'Transaction created successfully!'}, status=201)
    return JsonResponse({'errors': transaction_form.errors}, status=400)
```