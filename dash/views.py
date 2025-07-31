```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id):
    account = Account.objects.get(id=account_id)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.user = request.user
            transaction.save()
            return redirect('account_detail', account_id=account.id)

    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    balance = account.get_balance()

    context = {
        'account': account,
        'form': form,
        'transactions': transactions,
        'balance': balance,
    }
    
    return render(request, 'account/manage_account.html', context)
```