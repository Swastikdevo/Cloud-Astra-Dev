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
            return redirect('account_list')
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'form': account_form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
def create_transaction(request):
    transaction_form = TransactionForm(request.POST)
    if transaction_form.is_valid():
        transaction = transaction_form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        return JsonResponse({'status': 'success', 'message': 'Transaction created successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid transaction data'}, status=400)
```