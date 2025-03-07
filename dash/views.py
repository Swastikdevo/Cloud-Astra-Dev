```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
        else:
            messages.error(request, 'Error creating account. Please try again.')
    
    accounts = Account.objects.filter(user=request.user)
    form = AccountForm()
    return render(request, 'bank/manage_account.html', {'accounts': accounts, 'form': form})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction completed successfully!')
            return redirect('make_transaction')
        else:
            messages.error(request, 'Error making transaction. Please check your inputs.')

    form = TransactionForm()
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'bank/make_transaction.html', {'form': form, 'transactions': transactions})

@login_required
def account_balance(request, account_id):
    account = Account.objects.get(pk=account_id, user=request.user)
    balance = account.calculate_balance()  # Assuming a method to calculate balance
    return JsonResponse({'balance': balance})
```