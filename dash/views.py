```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
import datetime

@login_required
def manage_account(request):
    user_accounts = Account.objects.filter(owner=request.user)
    transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.user = request.user
            transaction.date = datetime.datetime.now()
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    else:
        form = TransactionForm()

    context = {
        'user_accounts': user_accounts,
        'transactions': transactions,
        'form': form,
    }
    
    return render(request, 'bank/manage_account.html', context)
```