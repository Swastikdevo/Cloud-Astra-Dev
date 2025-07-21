```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@csrf_exempt
@login_required
def bank_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
        return render(request, 'bank/dashboard.html', {
            'accounts': accounts,
            'transactions': transactions,
            'account_form': AccountForm(),
            'transaction_form': TransactionForm()
        })
    
    elif request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('bank_view')

        elif 'create_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.account = Account.objects.get(id=request.POST['account_id'])
                transaction.save()
                return redirect('bank_view')

    return JsonResponse({'status': 'Invalid request'}, status=400)
```