```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_overview(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('account_overview')
    else:
        form = AccountForm()
    return render(request, 'bank/create_account.html', {'form': form})

@login_required
@require_POST
def make_transaction(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.user = request.user
        transaction.save()
        response_data = {
            'message': 'Transaction successful',
            'transaction_id': transaction.id
        }
        return JsonResponse(response_data, status=200)
    return JsonResponse({'errors': form.errors}, status=400)

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

@login_required
def delete_account(request, account_id):
    try:
        account = Account.objects.get(id=account_id, user=request.user)
        account.delete()
        return redirect('account_overview')
    except Account.DoesNotExist:
        return JsonResponse({'error': 'Account not found'}, status=404)

@login_required
def update_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_overview')
    else:
        form = AccountForm(instance=account)
    return render(request, 'bank/update_account.html', {'form': form, 'account': account})
```