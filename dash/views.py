```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request):
    """View function to manage bank account creation and transaction."""

    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid form data!'})
                
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid transaction data!'})

    elif request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')

        return render(request, 'manage_account.html', {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm(),
        })
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request method!'})
```