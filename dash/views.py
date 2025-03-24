```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from .forms import BankAccountForm, TransactionForm

@csrf_exempt
@login_required
def manage_bank_accounts(request):
    if request.method == 'POST':
        # Handle new account creation
        form = BankAccountForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            return JsonResponse({'message': 'Account created successfully!'})
        else:
            return JsonResponse({'error': form.errors}, status=400)

    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'bank/manage_accounts.html', {'accounts': accounts})

@login_required
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return JsonResponse({'message': 'Transaction successful!'})
        else:
            return JsonResponse({'error': form.errors}, status=400)

    return render(request, 'bank/make_transaction.html', {'form': TransactionForm()})

@login_required
def account_summary(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/account_summary.html', {'account': account, 'transactions': transactions})
```