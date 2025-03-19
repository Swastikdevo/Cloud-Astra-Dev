```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_management(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                account = account_form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('account_management')
        elif 'make_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return redirect('account_management')
    else:
        account_form = AccountForm()
        transaction_form = TransactionForm()

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)

    context = {
        'account_form': account_form,
        'transaction_form': transaction_form,
        'accounts': accounts,
        'transactions': transactions,
    }
    return render(request, 'bank/account_management.html', context)

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    context = {
        'account': account,
        'transactions': Transaction.objects.filter(account=account),
    }
    return render(request, 'bank/account_detail.html', context)

@login_required
def account_balance(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    return JsonResponse({'balance': account.balance})
```