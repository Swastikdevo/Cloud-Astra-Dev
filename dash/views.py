```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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
                messages.success(request, "Account created successfully!")
                return redirect('manage_account')
            else:
                messages.error(request, "Error creating account. Please correct the form.")

        if 'make_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, "Transaction made successfully!")
                return redirect('manage_account')
            else:
                messages.error(request, "Error making transaction. Please correct the form.")
    else:
        form = AccountForm()
        transaction_form = TransactionForm()

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'form': form,
        'transaction_form': transaction_form,
        'accounts': accounts,
        'transactions': transactions
    }
    
    return render(request, 'bank/manage_account.html', context)
```