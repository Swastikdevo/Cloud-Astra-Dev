```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request, account_id=None):
    if account_id:
        account = get_object_or_404(Account, id=account_id)
    else:
        account = None
    
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_detail', account_id=account.id)
    else:
        form = AccountForm(instance=account)
    
    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'bank/manage_account.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def transfer_funds(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.from_account = account
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
    else:
        form = TransactionForm()

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'bank/transfer_funds.html', context)

@login_required
@require_http_methods(["POST"])
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    if request.user == account.user:
        account.delete()
        return JsonResponse({'status': 'success', 'message': 'Account deleted successfully.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'You do not have permission to delete this account.'})
```