```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
def manage_account(request, account_id=None):
    if request.method == 'POST':
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Account updated successfully!'})
        else:
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'New account created successfully!'})
    else:
        if account_id:
            account = Account.objects.get(id=account_id)
            form = AccountForm(instance=account)
        else:
            form = AccountForm()

    return render(request, 'account/manage_account.html', {'form': form})

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Funds transferred successfully!'})
    else:
        form = TransactionForm()
    
    return render(request, 'transaction/transfer_funds.html', {'form': form})
```