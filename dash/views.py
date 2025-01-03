```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_management(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return JsonResponse({'success': True, 'message': 'Account created successfully!'})

    accounts = Account.objects.filter(user=request.user)
    form = AccountForm()
    return render(request, 'bank/account_management.html', {'accounts': accounts, 'form': form})

@login_required
def transaction_management(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.user = request.user
            new_transaction.save()
            return JsonResponse({'success': True, 'message': 'Transaction recorded successfully!'})

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    form = TransactionForm()
    return render(request, 'bank/transaction_management.html', {'transactions': transactions, 'form': form})
```