```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('account_dashboard')
    else:
        form = TransactionForm()

    return render(request, 'bank/create_transaction.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

@login_required
def account_summary(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    total_balance = account.balance
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'bank/account_summary.html', {'account': account, 'total_balance': total_balance, 'transactions': transactions})

@login_required
def ajax_balance_check(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    return JsonResponse({'balance': account.balance}, status=200)
```