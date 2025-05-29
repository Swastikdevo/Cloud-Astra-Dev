```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import BankAccount, Transaction
from .forms import BankAccountForm, TransactionForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "GET":
        accounts = BankAccount.objects.filter(user=request.user)
        form = BankAccountForm()
        return render(request, 'bank/manage_account.html', {'accounts': accounts, 'form': form})

    elif request.method == "POST":
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('manage_account')

@login_required
@require_http_methods(["GET", "POST"])
def transaction_history(request, account_id):
    account = BankAccount.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    if request.method == "GET":
        return render(request, 'bank/transaction_history.html', {'account': account, 'transactions': transactions})

    elif request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account
            transaction.save()
            return JsonResponse({'status': 'Success', 'transaction_id': transaction.id})

@login_required
@require_http_methods(["POST"])
def transfer_funds(request):
    source_account_id = request.POST.get('source_account_id')
    destination_account_id = request.POST.get('destination_account_id')
    amount = request.POST.get('amount')

    source_account = BankAccount.objects.get(id=source_account_id, user=request.user)
    destination_account = BankAccount.objects.get(id=destination_account_id)

    if source_account.balance >= float(amount):
        source_account.balance -= float(amount)
        destination_account.balance += float(amount)
        source_account.save()
        destination_account.save()

        Transaction.objects.create(account=source_account, amount=-float(amount), tx_type='Transfer')
        Transaction.objects.create(account=destination_account, amount=float(amount), tx_type='Transfer')

        return JsonResponse({'status': 'Success', 'message': 'Funds transferred successfully.'})
    else:
        return JsonResponse({'status': 'Error', 'message': 'Insufficient funds.'})
```