```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages


@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_list')
        else:
            messages.error(request, 'Error creating account. Please check your input.')

    form = AccountForm()
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'form': form, 'accounts': accounts})


@login_required
@csrf_exempt
def transaction_view(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('transaction_history', account_id=account_id)
        else:
            messages.error(request, 'Error processing transaction. Please check your input.')

    form = TransactionForm()
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'transaction_view.html', {'form': form, 'transactions': transactions, 'account': account})
```