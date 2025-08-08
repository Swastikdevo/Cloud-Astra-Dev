```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    if request.method == "POST":
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('account_management')
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('account_management')
    else:
        form = AccountForm()
        transaction_form = TransactionForm()

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__user=request.user)

    return render(request, 'account_management.html', {
        'form': form,
        'transaction_form': transaction_form,
        'accounts': accounts,
        'transactions': transactions
    })

@login_required
@require_http_methods(["POST"])
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    account.delete()
    return JsonResponse({'success': True})

@login_required
@require_http_methods(["POST"])
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, account__user=request.user)
    transaction.delete()
    return JsonResponse({'success': True})
```