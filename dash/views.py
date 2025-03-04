```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator

@login_required
def account_overview(request):
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        return JsonResponse({'message': 'Account created successfully!'})
    return JsonResponse({'error': form.errors}, status=400)

@login_required
def transaction_history(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

@login_required
@require_POST
def perform_transaction(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()
        return JsonResponse({'message': 'Transaction successful!'})
    return JsonResponse({'error': form.errors}, status=400)
```