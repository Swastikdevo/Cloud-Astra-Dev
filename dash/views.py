```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
    
    if request.method == 'POST':
        trans_form = TransactionForm(request.POST)
        if trans_form.is_valid():
            transaction = trans_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('account_dashboard')
    else:
        trans_form = TransactionForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'transaction_form': trans_form,
    }
    
    return render(request, 'bank/account_dashboard.html', context)

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_dashboard')
    else:
        form = AccountForm()

    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == 'POST':
        account.delete()
        return redirect('account_dashboard')
    return render(request, 'bank/delete_account.html', {'account': account})

@login_required
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

@login_required
def ajax_balance(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    balance = account.balance
    return JsonResponse({'balance': balance})
```