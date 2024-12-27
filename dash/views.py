```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    # Retrieve the user's account details
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.account = account
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('manage_account')
        else:
            messages.error(request, 'Error in transaction form. Please check the details.')
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'form': form,
        'transactions': transactions,
    }
    
    return render(request, 'bank/manage_account.html', context)
```