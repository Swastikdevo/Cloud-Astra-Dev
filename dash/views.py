```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id):
    """View to manage a bank account including creating transactions."""
    account = Account.objects.get(id=account_id)

    if request.method == "POST":
        if 'transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.account = account
                transaction.user = request.user
                transaction.save()
                messages.success(request, "Transaction successfully added!")
                return redirect('manage_account', account_id=account.id)
        elif 'update' in request.POST:
            account_form = AccountForm(request.POST, instance=account)
            if account_form.is_valid():
                account_form.save()
                messages.success(request, "Account details updated successfully.")
                return redirect('manage_account', account_id=account.id)
    else:
        transaction_form = TransactionForm()
        account_form = AccountForm(instance=account)

    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'transaction_form': transaction_form,
        'account_form': account_form,
        'transactions': transactions,
    }
    return render(request, 'bank/manage_account.html', context)
```