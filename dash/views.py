```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def manage_bank(request):
    if request.method == 'POST':
        if 'add_account' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'status': 'Account created successfully!'})
        
        elif 'make_transaction' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'Transaction recorded successfully!'})
            
    else:
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(user=request.user)
        account_form = AccountForm()
        transaction_form = TransactionForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': account_form,
        'transaction_form': transaction_form,
    }
    return render(request, 'bank/manage_bank.html', context)
```