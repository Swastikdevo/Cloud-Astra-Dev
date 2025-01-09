```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_overview')

    accounts = Account.objects.filter(user=request.user)
    form = AccountForm()
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = TransactionForm()
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/make_transaction.html', {'form': form, 'accounts': accounts})

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})
```