```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
def manage_accounts(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_accounts')
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_accounts.html', {'accounts': accounts, 'account_form': account_form})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return JsonResponse({'status': 'success', 'message': 'Transaction completed'}, status=200)

    else:
        transaction_form = TransactionForm()

    return render(request, 'bank/make_transaction.html', {'transaction_form': transaction_form})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/view_transactions.html', {'transactions': transactions})

@login_required
def delete_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted successfully!')
        return redirect('manage_accounts')

    return render(request, 'bank/delete_account.html', {'account': account})
```