```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account

            if transaction.transaction_type == 'withdrawal':
                if account.balance >= transaction.amount:
                    account.balance -= transaction.amount
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient balance!')
                    return redirect('manage_account')
            elif transaction.transaction_type == 'deposit':
                account.balance += transaction.amount
                messages.success(request, 'Deposit successful!')
            
            # Save the transaction and update the account
            transaction.save()
            account.save()
            return redirect('manage_account')
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/manage_account.html', {
        'account': account,
        'form': form,
        'transactions': transactions
    })
```