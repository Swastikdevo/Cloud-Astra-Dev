```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__user=request.user)
        account_form = AccountForm()
        transaction_form = TransactionForm()
        return render(request, 'bank_management.html', {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': account_form,
            'transaction_form': transaction_form,
        })

    elif request.method == 'POST':
        if 'create_account' in request.POST:
            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                account = account_form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})

        elif 'make_transaction' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.account = Account.objects.get(id=request.POST['account_id'], user=request.user)
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid form submission.'})
```