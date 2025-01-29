```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import BankAccount, Transaction
from .forms import BankAccountForm, TransactionForm

@login_required
def bank_account_view(request, account_id):
    account = get_object_or_404(BankAccount, id=account_id, user=request.user)

    if request.method == 'POST':
        if 'update_account' in request.POST:
            form = BankAccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return redirect('bank_account_view', account_id=account.id)
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = account
                transaction.save()
                return redirect('bank_account_view', account_id=account.id)

    else:
        form = BankAccountForm(instance=account)
        transaction_form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'form': form,
        'transaction_form': transaction_form,
        'transactions': transactions,
    }
    return render(request, 'bank_management/bank_account.html', context)

@login_required
def transaction_history_view(request, account_id):
    account = get_object_or_404(BankAccount, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'bank_management/transaction_history.html', {'transactions': transactions})

@login_required
def account_balance_view(request, account_id):
    account = get_object_or_404(BankAccount, id=account_id, user=request.user)
    balance = account.get_balance()
    
    return JsonResponse({'account_id': account.id, 'balance': balance})
```