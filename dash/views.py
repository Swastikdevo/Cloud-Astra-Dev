```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            # Add the transaction to the relevant account
            account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
            account.balance += form.cleaned_data['amount']
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form submission.'})

@csrf_exempt
@login_required
def view_transactions(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'account/view_transactions.html', {'transactions': transactions, 'account': account})
```