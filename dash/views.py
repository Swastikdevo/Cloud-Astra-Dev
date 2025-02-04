```python
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(['GET', 'POST'])
def manage_account(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        # Handling deposit
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)

        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            messages.success(request, f'Deposit successful! New balance: {account.balance}')
            return redirect('manage_account')

        elif withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            if amount > account.balance:
                messages.error(request, 'Insufficient funds for withdrawal.')
            else:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                messages.success(request, f'Withdrawal successful! New balance: {account.balance}')
                return redirect('manage_account')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    return render(request, 'bank/manage_account.html', context)
```