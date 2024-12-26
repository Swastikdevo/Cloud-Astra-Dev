```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    # Handle account creation
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        account_form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'account_form': account_form, 'accounts': accounts})

@login_required
@require_http_methods(["GET", "POST"])
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('transaction_history', account_id=account.id)
    else:
        transaction_form = TransactionForm()

    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions, 'transaction_form': transaction_form})

@login_required
@require_http_methods(["POST"])
def transfer_funds(request, account_id):
    from_account = Account.objects.get(id=account_id, user=request.user)
    to_account_id = request.POST.get('to_account_id')
    amount = request.POST.get('amount')

    if amount and to_account_id:
        to_account = Account.objects.get(id=to_account_id)
        if from_account.balance >= float(amount):
            from_account.balance -= float(amount)
            to_account.balance += float(amount)
            from_account.save()
            to_account.save()
            Transaction.objects.create(account=from_account, amount=-float(amount), description='Transfer to Account {}'.format(to_account_id))
            Transaction.objects.create(account=to_account, amount=float(amount), description='Transfer from Account {}'.format(account_id))
            return HttpResponse('Transfer successful')
        else:
            return HttpResponse('Insufficient funds', status=400)

    return HttpResponse('Invalid transfer request', status=400)
```