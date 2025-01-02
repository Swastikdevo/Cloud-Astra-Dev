```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
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

        elif action == 'make_transaction':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Transaction completed successfully!'})

    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': AccountForm(),
        'transaction_form': TransactionForm(),
    }
    return render(request, 'bank_management.html', context)
```