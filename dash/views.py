```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
def account_dashboard(request):
    accounts = Account.objects.filter(owner=request.user).all()
    return render(request, 'bank/dashboard.html', {'accounts': accounts})

@csrf_exempt
@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.owner = request.user
            new_account.save()
            return JsonResponse({'status': 'Account created', 'account_id': new_account.id})
    else:
        form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def make_transaction(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'Transaction successful', 'transaction_id': transaction.id})
    else:
        form = TransactionForm()
    return render(request, 'bank/make_transaction.html', {'form': form, 'account': account})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})

@login_required
def view_balance(request, account_id):
    account = Account.objects.get(id=account_id, owner=request.user)
    return JsonResponse({'balance': account.balance})
```