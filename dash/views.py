```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
def manage_account(request):
    user_accounts = Account.objects.filter(user=request.user)

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

    return render(request, 'bank/manage_account.html', {
        'account_form': account_form,
        'user_accounts': user_accounts
    })

@login_required
def transactions(request):
    user_transactions = Transaction.objects.filter(account__user=request.user)

    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.account = transaction_form.cleaned_data['account']
            transaction.save()
            messages.success(request, 'Transaction recorded successfully.')
            return redirect('transactions')
    else:
        transaction_form = TransactionForm()

    return render(request, 'bank/transactions.html', {
        'transaction_form': transaction_form,
        'user_transactions': user_transactions
    })

@login_required
def get_balance(request, account_id):
    account = Account.objects.filter(id=account_id, user=request.user).first()
    if account:
        balance = account.balance
        return JsonResponse({'balance': balance})
    return JsonResponse({'error': 'Account not found.'}, status=404)
```