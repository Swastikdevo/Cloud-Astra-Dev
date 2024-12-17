```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if account_id:
        account = Account.objects.get(id=account_id)
    else:
        account = None

    if request.method == 'POST':
        if account:
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user  # Assuming Account has a ForeignKey to User
            account.save()
            return redirect('account_details', account_id=account.id)
    else:
        form = AccountForm(instance=account)

    return render(request, 'manage_account.html', {'form': form, 'account': account})

@login_required
@require_http_methods(["POST"])
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id)
    form = TransactionForm(request.POST)

    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.user = request.user  # Assuming Transaction has a ForeignKey to User
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    return JsonResponse({'status': 'error', 'errors': form.errors})
```