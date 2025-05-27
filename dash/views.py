```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_management')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_management.html', {'form': form, 'accounts': accounts})

@login_required
@csrf_exempt
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

@login_required
@csrf_exempt
def initiate_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return JsonResponse({'status': 'success', 'message': 'Transaction completed!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data!'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'}, status=405)
```