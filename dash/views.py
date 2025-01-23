```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
def bank_manage_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
        return render(request, 'bank/manage.html', {'accounts': accounts, 'transactions': transactions})

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
                new_transaction = form.save(commit=False)
                new_transaction.account = Account.objects.get(id=request.POST.get('account_id'), user=request.user)
                new_transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction recorded successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
```