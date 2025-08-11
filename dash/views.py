```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'create' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('account_success')
        
        elif 'transact' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = Account.objects.get(id=request.POST['account_id'])
                transaction.save()
                return redirect('transaction_success')

    else:
        account_form = AccountForm()
        transaction_form = TransactionForm()
        accounts = Account.objects.filter(user=request.user)
    
    return render(request, 'bank/manage_account.html', {
        'account_form': account_form,
        'transaction_form': transaction_form,
        'accounts': accounts,
    })
```