```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.owner = request.user
            new_account.save()
            return redirect('account_overview')
    else:
        form = AccountForm()

    return render(request, 'accounts/overview.html', {
        'accounts': user_accounts,
        'form': form
    })

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'transactions/history.html', {
        'account': account,
        'transactions': transactions
    })

@login_required
def perform_transaction(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'Transaction successful'})
        else:
            return JsonResponse({'status': 'Transaction failed', 'errors': form.errors}, status=400)

    form = TransactionForm()
    return render(request, 'transactions/perform.html', {
        'account': account,
        'form': form
    })
```