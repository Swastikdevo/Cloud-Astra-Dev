```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    user = request.user
    try:
        account = Account.objects.get(user=user)
    except Account.DoesNotExist:
        account = None

    if request.method == 'POST':
        if 'update' in request.POST:
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account details updated successfully.')
                return redirect('manage_account')
        elif 'transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.account = account
                transaction.save()
                messages.success(request, 'Transaction completed successfully.')
                return redirect('manage_account')
    else:
        account_form = AccountForm(instance=account)
        transaction_form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account_form': account_form,
        'transaction_form': transaction_form,
        'transactions': transactions,
        'account': account,
    }
    return render(request, 'bank/manage_account.html', context)
```