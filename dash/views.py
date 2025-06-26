```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.utils.decorators import method_decorator

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == "POST":
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.user = request.user
                new_account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})

        elif 'create_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                new_transaction = form.save(commit=False)
                new_transaction.account = Account.objects.get(id=request.POST['account_id'])
                new_transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction created successfully.'})

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid action'})

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__user=request.user)
    
    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': AccountForm(),
        'transaction_form': TransactionForm(),
    })
```