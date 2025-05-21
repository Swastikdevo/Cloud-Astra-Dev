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
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        form = AccountForm()
        return render(request, 'bank/manage_account.html', {'accounts': accounts, 'form': form})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to create account.', 'errors': form.errors})

@csrf_exempt
@login_required
def transact(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(account__user=request.user)
        form = TransactionForm()
        return render(request, 'bank/transact.html', {'transactions': transactions, 'form': form})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = form.cleaned_data['account']
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to record transaction.', 'errors': form.errors})
```