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
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': form.errors})

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
        else:
            return JsonResponse({'status': 'error', 'message': form.errors})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/view_transactions.html', {'transactions': transactions})
```