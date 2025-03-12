```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransactionForm
from django.contrib import messages
from decimal import Decimal

@login_required
def manage_account(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            transaction_type = form.cleaned_data['transaction_type']
            account = Account.objects.get(user=request.user)

            if transaction_type == 'deposit':
                account.balance += Decimal(amount)
                account.save()
                transaction = Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Deposit',
                )
                messages.success(request, f'Deposit successful! New balance: {account.balance}')
            elif transaction_type == 'withdrawal':
                if account.balance >= Decimal(amount):
                    account.balance -= Decimal(amount)
                    account.save()
                    transaction = Transaction.objects.create(
                        account=account,
                        amount=amount,
                        transaction_type='Withdrawal',
                    )
                    messages.success(request, f'Withdrawal successful! New balance: {account.balance}')
                else:
                    messages.error(request, 'Insufficient funds for withdrawal!')
            return redirect('manage_account')
    else:
        form = TransactionForm()

    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    return render(request, 'bank/manage_account.html', {'form': form, 'transactions': transactions})
```