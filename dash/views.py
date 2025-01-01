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
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid form data.'}, status=400)
    
    elif request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'manage_account.html', {'accounts': accounts, 'form': AccountForm()})

@login_required
@csrf_exempt
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid transaction data.'}, status=400)

    elif request.method == 'GET':
        transactions = Transaction.objects.filter(user=request.user)
        return render(request, 'transactions.html', {'transactions': transactions, 'form': TransactionForm()})
```