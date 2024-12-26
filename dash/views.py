```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = user_account
            transaction.save()

            # Update account balance
            if transaction.type == 'deposit':
                user_account.balance += transaction.amount
            elif transaction.type == 'withdrawal':
                user_account.balance -= transaction.amount
            user_account.save()
            return redirect('account_summary')

    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    context = {
        'user_account': user_account,
        'form': form,
        'transactions': transactions
    }
    
    return render(request, 'manage_account.html', context)
```