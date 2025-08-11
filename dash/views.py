```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully.')
            return redirect('manage_account')
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'account_form': account_form, 'accounts': accounts})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully.')
            return JsonResponse({'status': 'success', 'message': 'Transaction completed!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid transaction data.'})

    transaction_form = TransactionForm()
    return render(request, 'bank/make_transaction.html', {'transaction_form': transaction_form})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/view_transactions.html', {'transactions': transactions})
```