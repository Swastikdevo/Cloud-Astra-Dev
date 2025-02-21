```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        messages.success(request, 'Account created successfully!')
        return redirect('account_overview')
    else:
        messages.error(request, 'Error creating account.')
        return redirect('account_overview')

@login_required
@require_POST
def make_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        messages.success(request, 'Transaction completed successfully!')
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        messages.error(request, 'Error processing transaction.')
        return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})
```