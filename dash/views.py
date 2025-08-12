```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

@csrf_exempt
@login_required
def bank_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
        account_form = AccountForm()
        transaction_form = TransactionForm()
        return render(request, 'bank_management.html', {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': account_form,
            'transaction_form': transaction_form
        })

    elif request.method == 'POST':
        if request.POST.get('action') == 'create_account':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'account_id': account.id})

        elif request.POST.get('action') == 'make_transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = Account.objects.get(id=request.POST['account_id'], user=request.user)
                transaction.save()
                return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
```