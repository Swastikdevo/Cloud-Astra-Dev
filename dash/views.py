```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def transaction_view(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'form': form,
        'transactions': transactions,
    }
    return render(request, 'bank/transaction_detail.html', context)

@login_required
@require_http_methods(["GET"])
def account_balance(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    balance = account.balance

    return JsonResponse({'account_id': account_id, 'balance': balance})
```