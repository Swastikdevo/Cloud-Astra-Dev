```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import CreateAccountForm, DepositForm, WithdrawForm

@login_required
def manage_account(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                new_account = form.save(commit=False)
                new_account.owner = user
                new_account.save()
                messages.success(request, 'Account created successfully.')
            else:
                messages.error(request, 'Error creating account.')

        elif action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                transaction = Transaction(account=account, amount=amount, transaction_type='deposit')
                transaction.save()
                messages.success(request, 'Deposit successful.')
            else:
                messages.error(request, 'Error processing deposit.')

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    transaction = Transaction(account=account, amount=amount, transaction_type='withdraw')
                    transaction.save()
                    messages.success(request, 'Withdrawal successful.')
                else:
                    messages.error(request, 'Insufficient funds.')
            else:
                messages.error(request, 'Error processing withdrawal.')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    create_account_form = CreateAccountForm()

    return render(request, 'manage_account.html', {
        'accounts': accounts,
        'create_account_form': create_account_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```