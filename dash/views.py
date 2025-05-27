```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
import datetime

@login_required
def manage_account(request):
    accounts = Account.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = get_object_or_404(Account, id=request.POST['account_id'], user=request.user)
            transaction.date = datetime.datetime.now()
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    else:
        form = TransactionForm()

    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'form': form,
    })

@login_required
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'bank/account_details.html', {
        'account': account,
        'transactions': transactions,
    })
```