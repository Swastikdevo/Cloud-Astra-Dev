```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
def manage_account(request, account_id=None):
    if account_id:
        account = Account.objects.get(id=account_id)
    else:
        account = None
    
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account details saved successfully!')
            return redirect('manage_account', account_id=form.instance.id)
    else:
        form = AccountForm(instance=account)
    
    return render(request, 'bank/manage_account.html', {'form': form, 'account': account})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=form.cleaned_data['account_id'])
            transaction.save()
            messages.success(request, 'Transaction created successfully!')
            return redirect('transaction_history')
    else:
        form = TransactionForm()
    
    return render(request, 'bank/create_transaction.html', {'form': form})

@login_required
def delete_account(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted successfully!')
        return redirect('account_list')
    
    return render(request, 'bank/delete_account.html', {'account': account})
```