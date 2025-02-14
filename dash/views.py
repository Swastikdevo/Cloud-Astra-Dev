```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_detail', account_id=account.id)
        else:
            messages.error(request, 'Error creating account. Please check the form.')

    accounts = Account.objects.filter(user=request.user)
    form = AccountForm()
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
def perform_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        messages.success(request, 'Transaction completed successfully!')
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        messages.error(request, 'Transaction failed. Please check your details.')
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@login_required
@require_http_methods(["GET"])
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})
```