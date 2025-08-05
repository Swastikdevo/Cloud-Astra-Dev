```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import AccountForm, DepositForm, WithdrawalForm
from django.contrib import messages

@login_required
def manage_account(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        if 'create' in request.POST:
            form = AccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.owner = user
                new_account.save()
                messages.success(request, 'Account created successfully!')
                return redirect('manage_account')

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.deposit(amount)
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('manage_account')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.withdraw(amount):
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account')

    else:
        form = AccountForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'bank/manage_account.html', {
        'accounts': accounts,
        'form': form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```