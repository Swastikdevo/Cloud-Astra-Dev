```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {
        'account_form': account_form,
        'accounts': accounts,
    })

@login_required
@require_http_methods(["POST"])
def make_transaction(request):
    transaction_form = TransactionForm(request.POST)
    if transaction_form.is_valid():
        transaction = transaction_form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        messages.success(request, 'Transaction completed successfully!')
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        return JsonResponse({'status': 'error', 'errors': transaction_form.errors}, status=400)

@login_required
@require_http_methods(["GET"])
def account_summary(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        transactions = Transaction.objects.filter(account=account).order_by('-date')
        return render(request, 'bank/account_summary.html', {
            'account': account,
            'transactions': transactions,
        })
    except Account.DoesNotExist:
        messages.error(request, 'Account not found.')
        return redirect('manage_account')
```