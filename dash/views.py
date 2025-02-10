```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                messages.success(request, 'Account created successfully.')
                return redirect('bank_management')
            else:
                messages.error(request, 'Error creating account.')

        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                messages.success(request, 'Transaction completed successfully.')
                return redirect('bank_management')
            else:
                messages.error(request, 'Error completing transaction.')
    
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)

    return render(request, 'bank_management.html', {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': AccountForm(),
        'transaction_form': TransactionForm()
    })
```