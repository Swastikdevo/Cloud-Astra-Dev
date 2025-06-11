```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def transaction_create(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()

        # Update account balance after transaction
        account = Account.objects.get(id=form.cleaned_data['account'].id)
        account.balance += transaction.amount if transaction.transaction_type == 'credit' else -transaction.amount
        account.save()

        messages.success(request, 'Transaction recorded successfully!')
        return redirect('account_dashboard')
    else:
        messages.error(request, 'Error in transaction. Please correct the form.')
        return redirect('account_dashboard')

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

@login_required
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
def delete_transaction(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id, user=request.user)
    account = transaction.account
    if transaction.transaction_type == 'credit':
        account.balance -= transaction.amount
    else:
        account.balance += transaction.amount
    account.save()
    transaction.delete()

    messages.success(request, 'Transaction deleted successfully!')
    return redirect('transaction_history')
```