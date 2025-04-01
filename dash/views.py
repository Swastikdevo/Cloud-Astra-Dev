```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if account_id:
        account = get_object_or_404(Account, id=account_id, user=request.user)
    else:
        account = None
    
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_detail', account_id=form.instance.id)
    else:
        form = AccountForm(instance=account)

    return render(request, 'bank/manage_account.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def transfer_funds(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.sender = account
            transaction.save()
            account.balance -= transaction.amount
            account.save()
            return redirect('transaction_history', account_id=account.id)
    else:
        form = TransactionForm()

    return render(request, 'bank/transfer_funds.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(sender=account)

    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})
```