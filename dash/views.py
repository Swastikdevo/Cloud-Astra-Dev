```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
def manage_account_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_account':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'account_id': account.id})

        elif action == 'deposit':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'transaction_id': transaction.id})

        elif action == 'withdraw':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'transaction_id': transaction.id})
        
        elif action == 'get_balance':
            account_id = request.POST.get('account_id')
            account = Account.objects.get(id=account_id, user=request.user)
            return JsonResponse({'balance': account.balance})

    else:
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'manage_account.html', {'accounts': accounts})
```