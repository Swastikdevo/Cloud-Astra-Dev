```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
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
            return redirect('manage_account')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'form': form, 'accounts': accounts})

@login_required
@require_http_methods(["POST"])
def transact(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        messages.success(request, 'Transaction completed successfully!')
        return JsonResponse({"status": "success", "message": "Transaction completed!"}, status=200)
    return JsonResponse({"status": "error", "message": "Transaction failed!"}, status=400)

@login_required
@require_http_methods(["GET"])
def account_details(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'account_details.html', {'account': account, 'transactions': transactions})
    except Account.DoesNotExist:
        messages.error(request, 'Account does not exist.')
        return redirect('manage_account')
```