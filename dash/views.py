```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'success': True, 'message': 'Account created successfully!'})
        
        elif 'perform_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'success': True, 'message': 'Transaction completed successfully!'})
        
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]
    account_form = AccountForm()
    transaction_form = TransactionForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': account_form,
        'transaction_form': transaction_form,
    }

    return render(request, 'bank/account_management.html', context)
```