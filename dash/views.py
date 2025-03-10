```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.db import transaction

@csrf_exempt
@login_required
def account_management(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_account':
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully!'})
            return JsonResponse({'status': 'error', 'message': 'Invalid form data!'})

        elif action == 'make_transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    transaction_instance = form.save(commit=False)
                    transaction_instance.user = request.user
                    transaction_instance.save()
                    # Update account balance as per transaction
                    account = Account.objects.get(id=form.cleaned_data['account'].id)
                    account.balance += transaction_instance.amount
                    account.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction successful!'})
            return JsonResponse({'status': 'error', 'message': 'Invalid transaction data!'})

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'bank/account_management.html', {'accounts': accounts, 'transactions': transactions})
```