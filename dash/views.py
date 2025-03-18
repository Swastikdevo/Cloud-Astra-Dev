```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(user=request.user)

    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('account_overview')

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    transaction_form = TransactionForm()

    context = {
        'user_accounts': user_accounts,
        'transactions': transactions,
        'transaction_form': transaction_form,
        'total_balance': sum(account.balance for account in user_accounts)
    }

    return render(request, 'bank/account_overview.html', context)

@login_required
def create_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_overview')
    else:
        form = AccountForm()

    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def delete_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == "POST":
        account.delete()
        return redirect('account_overview')
    return render(request, 'bank/delete_account.html', {'account': account})

@login_required
def account_balance_api(request):
    if request.method == "GET":
        user_accounts = Account.objects.filter(user=request.user)
        balance_info = {account.account_number: account.balance for account in user_accounts}
        return JsonResponse(balance_info)
```