```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('manage_account')

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@csrf_exempt
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    
    if request.method == 'GET':
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.account = account
            new_transaction.save()
            return redirect('transaction_history', account_id=account.id)

    return JsonResponse({'error': 'Invalid request'}, status=400)
```