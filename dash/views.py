```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is not valid!'})

    accounts = Account.objects.filter(user=request.user)
    form = AccountForm()
    return render(request, 'manage_account.html', {'accounts': accounts, 'form': form})

@login_required
def add_transaction(request, account_id):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(id=account_id, user=request.user)
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction added successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Form is not valid!'})

    form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form, 'account_id': account_id})
```