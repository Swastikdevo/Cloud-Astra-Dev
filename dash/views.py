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
    if request.method == 'GET':
        if account_id:
            account = Account.objects.get(pk=account_id)
            form = AccountForm(instance=account)
            transactions = Transaction.objects.filter(account=account)
            return render(request, 'bank/account_detail.html', {'account': account, 'form': form, 'transactions': transactions})
        else:
            form = AccountForm()
            return render(request, 'bank/account_form.html', {'form': form})

    elif request.method == 'POST':
        if account_id:
            account = Account.objects.get(pk=account_id)
            form = AccountForm(request.POST, instance=account)
        else:
            form = AccountForm(request.POST)

        if form.is_valid():
            account = form.save()
            return redirect('account_detail', account_id=account.id)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def create_transaction(request, account_id):
    if request.method == 'POST':
        account = Account.objects.get(pk=account_id)
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('account_detail', account_id=account.id)
    
    form = TransactionForm()
    return render(request, 'bank/transaction_form.html', {'form': form, 'account_id': account_id})
```