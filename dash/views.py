```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/account_management.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})

@login_required
@csrf_exempt
def transaction_history(request):
    if request.method == 'GET':
        account_id = request.GET.get('account_id')
        transactions = Transaction.objects.filter(account_id=account_id, account__user=request.user)
        return render(request, 'bank/transaction_history.html', {'transactions': transactions})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
```