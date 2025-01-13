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
        action = request.POST.get('action')

        if action == 'create':
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})

        elif action == 'update':
            account_id = request.POST.get('id')
            account = Account.objects.get(id=account_id)
            form = AccountForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Account updated successfully!'})
            else:
                return JsonResponse({'status': 'error', 'errors': form.errors})

        elif action == 'delete':
            account_id = request.POST.get('id')
            account = Account.objects.get(id=account_id)
            account.delete()
            return JsonResponse({'status': 'success', 'message': 'Account deleted successfully!'})

    else:
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'manage_account.html', {'accounts': accounts})

@login_required
@csrf_exempt
def manage_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully!'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'manage_transaction.html', {'transactions': transactions})
```