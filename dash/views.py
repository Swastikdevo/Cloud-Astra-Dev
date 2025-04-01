```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@require_http_methods(["GET", "POST"])
def account_management(request):
    if request.method == "POST":
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created successfully!')
                return redirect('account_management')
            else:
                messages.error(request, 'Error creating account. Please try again.')
        
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                account = Account.objects.get(id=request.POST['account_id'])
                transaction.account = account
                transaction.save()
                messages.success(request, 'Transaction completed successfully!')
                return redirect('account_management')
            else:
                messages.error(request, 'Error processing transaction. Please try again.')
    
    accounts = Account.objects.all()
    transactions = Transaction.objects.all()
    context = {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': AccountForm(),
        'transaction_form': TransactionForm(),
    }
    
    return render(request, 'bank/account_management.html', context)
```