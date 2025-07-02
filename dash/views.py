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
    if request.method == "POST":
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            new_account = account_form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('account_list')
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {
        'account_form': account_form,
        'accounts': accounts,
    })

@login_required
@require_http_methods(["GET", "POST"])
def transaction_history(request):
    if request.method == "POST":
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            new_transaction = transaction_form.save(commit=False)
            new_transaction.user = request.user
            new_transaction.save()
            return JsonResponse({"success": True, "message": "Transaction recorded successfully."})
    else:
        transaction_form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {
        'transaction_form': transaction_form,
        'transactions': transactions,
    })

@login_required
@require_http_methods(["GET"])
def account_summary(request):
    accounts = Account.objects.filter(user=request.user)
    total_balance = sum(account.balance for account in accounts)
    return render(request, 'bank/account_summary.html', {
        'accounts': accounts,
        'total_balance': total_balance,
    })
```