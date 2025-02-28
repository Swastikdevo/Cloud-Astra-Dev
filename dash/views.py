```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountCreationForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountCreationForm()

    accounts = Account.objects.filter(user=request.user)
    context = {
        'form': form,
        'accounts': accounts
    }
    return render(request, 'bank/manage_account.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def initiate_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_success', transaction_id=transaction.id)
    else:
        form = TransactionForm()

    context = {
        'form': form,
    }
    return render(request, 'bank/initiate_transaction.html', context)
```