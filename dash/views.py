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
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=200)
    else:
        form = TransactionForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/make_transaction.html', {'form': form, 'accounts': accounts})

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})
```