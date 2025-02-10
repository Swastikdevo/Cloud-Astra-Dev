```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account_management.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid form submission!'})

@method_decorator(login_required, name='dispatch')
@csrf_exempt
def process_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction processed successfully!'})
        return JsonResponse({'status': 'error', 'message': 'Invalid transaction data!'})

    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed!'})
```