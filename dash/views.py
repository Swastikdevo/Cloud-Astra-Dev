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
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__in=accounts)
        return render(request, 'bank_management.html', {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm()
        })
    
    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_account':
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})

        elif action == 'make_transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = Account.objects.get(id=request.POST.get('account_id'))
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully.'})

        return JsonResponse({'status': 'error', 'message': 'Invalid action or data.'})
```