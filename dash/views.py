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
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'accounts': accounts, 'form': AccountForm()})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

@login_required
def add_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction added successfully!'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': form.errors}, status=400)

    return render(request, 'bank/add_transaction.html', {'form': TransactionForm(), 'account': account})
```