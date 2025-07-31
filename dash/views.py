```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
def bank_management_view(request):
    if request.method == 'POST':
        # Handle new account creation
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_form.save()
            return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})

        # Handle new transaction creation
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            account = Account.objects.get(id=transaction_form.cleaned_data['account_id'])
            transaction.balance_after = account.balance + transaction.amount if transaction.type == 'credit' else account.balance - transaction.amount
            transaction.save()
            account.balance = transaction.balance_after
            account.save()
            return JsonResponse({'status': 'success', 'message': 'Transaction successful.'})

        return JsonResponse({'status': 'error', 'message': 'Form data is invalid.'})

    # On GET request, display accounts and transactions
    accounts = Account.objects.all()
    transactions = Transaction.objects.all()
    return render(request, 'bank_management.html', {'accounts': accounts, 'transactions': transactions})
```