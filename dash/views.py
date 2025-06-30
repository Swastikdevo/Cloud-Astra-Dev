```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def create_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('account_detail', account_id=new_account.id)
    else:
        form = AccountForm()

    return render(request, 'bank/create_account.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def make_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.user = request.user
            new_transaction.save()
            return redirect('transaction_history')
    else:
        form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'form': form})

@login_required
def account_details(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_details.html', {'account': account, 'transactions': transactions})
```