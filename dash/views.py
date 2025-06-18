```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import TransactionForm, AccountForm

@login_required
def manage_bank_account(request):
    user = request.user
    account = Account.objects.get(user=user)
    transactions = Transaction.objects.filter(account=account).order_by('-date_created')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount:.2f} successfully!')
                return redirect('manage_bank_account')
        elif 'withdraw' in request.POST:
            form = TransactionForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrew ${amount:.2f} successfully!')
                    return redirect('manage_bank_account')
                else:
                    messages.error(request, 'Insufficient funds for this withdrawal.')

    else:
        form = TransactionForm()

    context = {
        'account': account,
        'transactions': transactions,
        'form': form,
    }
    return render(request, 'bank/manage_account.html', context)
```