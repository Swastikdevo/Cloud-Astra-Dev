```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankAccount, Transaction
from .forms import BankAccountForm, TransactionForm
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
def account_overview(request):
    accounts = BankAccount.objects.filter(user=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': accounts})

@require_GET
@login_required
def view_account(request, account_id):
    try:
        account = BankAccount.objects.get(id=account_id, user=request.user)
    except BankAccount.DoesNotExist:
        messages.error(request, "Account does not exist.")
        return redirect('account_overview')
    
    transactions = Transaction.objects.filter(account=account)
    return render(request, 'bank/view_account.html', {'account': account, 'transactions': transactions})

@require_POST
@login_required
def create_account(request):
    form = BankAccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user
        account.save()
        messages.success(request, "Account created successfully.")
        return redirect('account_overview')
    else:
        messages.error(request, "Failed to create account. Please correct the errors.")
    return render(request, 'bank/create_account.html', {'form': form})

@require_POST
@login_required
def make_transaction(request, account_id):
    try:
        account = BankAccount.objects.get(id=account_id, user=request.user)
    except BankAccount.DoesNotExist:
        return JsonResponse({'error': 'Account not found.'}, status=404)

    form = TransactionForm(request.POST)
    if form.is_valid():
        transaction = form.save(commit=False)
        transaction.account = account
        transaction.save()
        messages.success(request, "Transaction completed successfully.")
        return JsonResponse({'message': 'Transaction successful.'}, status=200)
    else:
        return JsonResponse({'error': 'Transaction failed. Please correct the errors.'}, status=400)

@require_GET
@login_required
def transaction_history(request, account_id):
    try:
        account = BankAccount.objects.get(id=account_id, user=request.user)
        transactions = Transaction.objects.filter(account=account)
        return render(request, 'bank/transaction_history.html', {'transactions': transactions, 'account': account})
    except BankAccount.DoesNotExist:
        messages.error(request, "Account does not exist.")
        return redirect('account_overview')
```