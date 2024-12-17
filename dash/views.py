```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import AccountCreationForm, TransactionForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            form = AccountCreationForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Account creation failed!'})
        
        elif action == 'transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Transaction failed!'})

    # Retrieve user accounts and transactions for rendering in the template
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': AccountCreationForm(),
        'transaction_form': TransactionForm(),
    })
```