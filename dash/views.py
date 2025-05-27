```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        account_form = AccountForm()
        transaction_form = TransactionForm()
        return render(request, 'bank/manage_account.html', {
            'accounts': accounts,
            'account_form': account_form,
            'transaction_form': transaction_form,
        })

    elif request.method == 'POST':
        # Handling account creation
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            new_account = account_form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return redirect('manage_account')

    return render(request, 'bank/manage_account.html', {'account_form': account_form})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'status': 'success', 'transaction_id': transaction.id}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
```