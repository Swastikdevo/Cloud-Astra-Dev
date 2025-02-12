```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'manage_account.html', {'accounts': accounts})


@login_required
@csrf_exempt
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'message': 'Transaction recorded successfully!'}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)

    return render(request, 'create_transaction.html', {'account': account})


@login_required
def account_summary(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts)
    return render(request, 'account_summary.html', {'accounts': accounts, 'transactions': transactions})
```