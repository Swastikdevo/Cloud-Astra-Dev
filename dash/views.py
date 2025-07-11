```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import TransactionForm


@login_required
def manage_account(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = get_object_or_404(Account, id=request.POST.get('account_id'), owner=user)
            transaction.save()
            return redirect('manage_account')
    else:
        form = TransactionForm()

    context = {
        'accounts': accounts,
        'form': form,
    }
    return render(request, 'bank/manage_account.html', context)


@login_required
def view_transactions(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'bank/view_transactions.html', context)
```