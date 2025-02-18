```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
@csrf_exempt
def account_management_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_account':
            form = AccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Account created successfully.'})

        elif action == 'deposit':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})

        elif action == 'withdraw':
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                if transaction.amount > transaction.account.balance:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
                transaction.user = request.user
                transaction.save()
                return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'})

    else:
        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(user=request.user)
        account_form = AccountForm()
        transaction_form = TransactionForm()
        
    return render(request, 'account_management.html', {
        'accounts': accounts,
        'transactions': transactions,
        'account_form': account_form,
        'transaction_form': transaction_form,
    })
```