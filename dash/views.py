```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request, account_id=None):
    if request.method == 'GET':
        if account_id:
            account = get_object_or_404(Account, id=account_id)
            return render(request, 'account_detail.html', {'account': account})
        else:
            accounts = Account.objects.filter(user=request.user)
            return render(request, 'account_list.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('manage_account')
        else:
            return render(request, 'account_form.html', {'form': form})

@login_required
@csrf_exempt
def transaction_view(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'GET':
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'transaction_list.html', {'transactions': transactions, 'account': account})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'message': 'Transaction added successfully!'})
        else:
            return JsonResponse({'error': 'Invalid data'}, status=400)
```