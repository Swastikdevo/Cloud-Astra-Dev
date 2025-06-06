```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm, AccountForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('manage_account')
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return redirect('manage_account')
    else:
        form = TransactionForm()
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(user=request.user)

    return render(request, 'bank/manage_account.html', {
        'form': form,
        'accounts': accounts,
        'transactions': transactions,
    })
```