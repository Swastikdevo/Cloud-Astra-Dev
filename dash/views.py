```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_account':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})
            return JsonResponse({'status': 'error', 'message': 'Failed to create account.', 'errors': form.errors})

        elif action == 'make_transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully.'})
            return JsonResponse({'status': 'error', 'message': 'Failed to complete transaction.', 'errors': form.errors})

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    context = {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': AccountForm(),
        'transaction_form': TransactionForm(),
    }
    return render(request, 'bank_management.html', context)
```