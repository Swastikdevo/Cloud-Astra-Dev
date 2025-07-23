```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
@require_POST
def create_account(request):
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        return JsonResponse({'status': 'success', 'account_id': account.id})
    return JsonResponse({'status': 'error', 'errors': form.errors})

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.sender = request.user.account_set.get(id=request.POST['sender_account'])
            transaction.receiver = Account.objects.get(id=request.POST['receiver_account'])
            transaction.save()
            return redirect('account_overview')
    else:
        form = TransactionForm()
    return render(request, 'bank/transfer_funds.html', {'form': form})

@login_required
def transaction_history(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(sender=account) | Transaction.objects.filter(receiver=account)
    return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})
```