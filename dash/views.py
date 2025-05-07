```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction processed successfully.'}, status=200)
    else:
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    form = TransactionForm()
    
    context = {
        'accounts': accounts,
        'transactions': transactions,
        'form': form,
    }
    
    return render(request, 'bank/manage_account.html', context)

@login_required
def account_details(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    context = {
        'account': account,
        'transactions': transactions,
    }
    
    return render(request, 'bank/account_details.html', context)
```