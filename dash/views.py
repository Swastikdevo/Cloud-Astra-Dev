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
    if request.method == "POST":
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_form.save()
            return redirect('manage_accounts')
    else:
        account_form = AccountForm()
    
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_accounts.html', {'account_form': account_form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
def perform_transaction(request):
    transaction_form = TransactionForm(request.POST)
    if transaction_form.is_valid():
        transaction = transaction_form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        return JsonResponse({'success': True, 'transaction_id': transaction.id})
    return JsonResponse({'success': False, 'errors': transaction_form.errors})

@login_required
def account_details(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'account_details.html', {'account': account, 'transactions': transactions})
```