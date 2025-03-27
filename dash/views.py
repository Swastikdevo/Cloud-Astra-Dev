```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
def bank_management_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_account':
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})

        elif action == 'make_transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully.'})

        elif action == 'view_balance':
            account_id = request.POST.get('account_id')
            account = Account.objects.filter(id=account_id).first()
            if account:
                return JsonResponse({'status': 'success', 'balance': account.balance})
            return JsonResponse({'status': 'error', 'message': 'Account not found.'})

        elif action == 'get_transactions':
            account_id = request.POST.get('account_id')
            transactions = Transaction.objects.filter(account_id=account_id).values()
            return JsonResponse({'status': 'success', 'transactions': list(transactions)})

    accounts = Account.objects.all()
    transactions = Transaction.objects.all()
    return render(request, 'bank_management.html', {'accounts': accounts, 'transactions': transactions})
```