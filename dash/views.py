```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_accounts(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'accounts/manage_accounts.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

@login_required
@csrf_exempt
def transact(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)

    if request.method == 'GET':
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'transactions/manage_transactions.html', {'transactions': transactions, 'account': account})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'message': 'Transaction recorded successfully!'}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)
```