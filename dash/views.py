```python
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.views.decorators.http import require_http_methods

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
        else:
            return render(request, 'account/manage_account.html', {'form': form})
    else:
        form = AccountForm()
    return render(request, 'account/manage_account.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def create_transaction(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return redirect('transaction_detail', transaction_id=transaction.id)
        else:
            return render(request, 'transaction/create_transaction.html', {'form': form, 'account': account})
    else:
        form = TransactionForm()
    return render(request, 'transaction/create_transaction.html', {'form': form, 'account': account})

@login_required
def account_summary(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    summary_data = {
        'account': account,
        'transactions': transactions
    }
    
    return render(request, 'account/account_summary.html', summary_data)

@login_required
def ajax_balance(request, account_id):
    if request.is_ajax():
        account = Account.objects.get(id=account_id, user=request.user)
        balance = account.get_balance()
        return JsonResponse({'balance': balance})
    return HttpResponseBadRequest("Invalid request.")
```