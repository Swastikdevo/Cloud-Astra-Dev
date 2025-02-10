```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def account_manager(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_manager')

    accounts = Account.objects.filter(user=request.user)
    form = AccountForm()
    return render(request, 'account_manager.html', {'accounts': accounts, 'form': form})

@login_required
@require_http_methods(["POST"])
def perform_transaction(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()
        return JsonResponse({'message': 'Transaction successful', 'transaction_id': transaction.id}, status=201)
    return JsonResponse({'errors': form.errors}, status=400)

@login_required
@require_http_methods(["GET"])
def transaction_history(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'transaction_history.html', {'transactions': transactions, 'account': account})
```