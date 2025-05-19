```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                messages.success(request, 'Account created successfully!')
                return redirect('manage_account')
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, 'Transaction completed successfully!')
                return redirect('manage_account')
    else:
        form = AccountForm()
        transaction_form = TransactionForm()

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    return render(request, 'bank/manage_account.html', {
        'form': form,
        'transaction_form': transaction_form,
        'accounts': accounts,
        'transactions': transactions
    })

@login_required
def account_detail(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            account.delete()
            messages.success(request, 'Account deleted successfully!')
            return redirect('manage_account')
    
    return render(request, 'bank/account_detail.html', {'account': account})
```