```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@csrf_exempt
@login_required
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            account = get_object_or_404(Account, id=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save()
            messages.success(request, 'Account saved successfully.')
            return redirect('account_detail', account_id=account.id)
        else:
            messages.error(request, 'Error saving account. Please correct the errors below.')

    else:
        form = AccountForm(instance=get_object_or_404(Account, id=account_id)) if account_id else AccountForm()

    return render(request, 'bank/manage_account.html', {'form': form})

@csrf_exempt
@login_required
def transaction_view(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction recorded successfully.')
            return redirect('account_detail', account_id=account.id)
        else:
            messages.error(request, 'Error recording transaction. Please check the details.')

    else:
        form = TransactionForm()

    return render(request, 'bank/transaction_view.html', {'form': form, 'account': account})

@login_required
def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/account_detail.html', {'account': account, 'transactions': transactions})

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted successfully.')
        return redirect('account_list')

    return render(request, 'bank/delete_account.html', {'account': account})
```