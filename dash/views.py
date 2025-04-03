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
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Account creation failed.'})

        elif action == 'create_transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = Account.objects.get(id=request.POST.get('account_id'))
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Transaction recording failed.'})

        elif action == 'get_balance':
            account = Account.objects.get(id=request.POST.get('account_id'), user=request.user)
            return JsonResponse({'status': 'success', 'balance': account.balance})

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__user=request.user)
    return render(request, 'bank_management.html', {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': AccountForm(),
        'transaction_form': TransactionForm()
    })
```