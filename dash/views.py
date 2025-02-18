```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm

@login_required
def account_management(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_management')
    else:
        form = AccountForm()

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_management.html', {'form': form, 'accounts': accounts})

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            sender_account = form.cleaned_data['sender_account']
            receiver_account = form.cleaned_data['receiver_account']
            amount = form.cleaned_data['amount']

            if sender_account.balance >= amount:
                sender_account.balance -= amount
                receiver_account.balance += amount
                sender_account.save()
                receiver_account.save()

                transaction = Transaction(sender=sender_account, receiver=receiver_account, amount=amount)
                transaction.save()

                messages.success(request, 'Transfer completed successfully!')
                return redirect('transfer_funds')
            else:
                messages.error(request, 'Insufficient balance for the transaction.')

    form = TransactionForm()
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/transfer_funds.html', {'form': form, 'accounts': accounts})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(sender__user=request.user).order_by('-date')
    return render(request, 'bank/view_transactions.html', {'transactions': transactions})

@login_required
def check_balance(request):
    accounts = Account.objects.filter(user=request.user)
    balance_data = {account.account_number: account.balance for account in accounts}
    return JsonResponse(balance_data)
```