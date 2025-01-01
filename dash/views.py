```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_GET
def view_account(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/view_account.html', {'account': account, 'transactions': transactions})

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        return JsonResponse({'status': 'success', 'account_id': account.id})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@login_required
@require_POST
def transfer_funds(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.sender_account = Account.objects.get(id=request.POST['sender_account_id'])
        transaction.receiver_account = Account.objects.get(id=request.POST['receiver_account_id'])
        transaction.save()
        return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

@login_required
@require_GET
def account_summary(request):
    accounts = Account.objects.filter(user=request.user)
    total_balance = sum(account.balance for account in accounts)
    return render(request, 'bank/account_summary.html', {'accounts': accounts, 'total_balance': total_balance})
```