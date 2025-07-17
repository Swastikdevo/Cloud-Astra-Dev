```python
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm
from django.contrib import messages

@require_http_methods(["GET", "POST"])
def manage_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposited ${amount} successfully.')
                return redirect('manage_account', account_id=account.id)

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds for this withdrawal.')
                else:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrew ${amount} successfully.')
                    return redirect('manage_account', account_id=account.id)

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    return render(request, 'bank/manage_account.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    })
```