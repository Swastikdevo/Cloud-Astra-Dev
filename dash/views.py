```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully.')
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/manage_account.html', {'form': form, 'accounts': accounts})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully.')
            return redirect('transaction_history')
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'bank/make_transaction.html', {'form': form, 'transactions': transactions})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

def api_balance(request):
    if request.method == 'GET':
        account_id = request.GET.get('account_id')
        try:
            account = Account.objects.get(id=account_id, user=request.user)
            return JsonResponse({'balance': account.balance})
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Account not found.'}, status=404)
```