```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm
from django.contrib import messages

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@login_required
@require_POST
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        source_account = form.cleaned_data['source_account']
        destination_account = form.cleaned_data['destination_account']
        amount = form.cleaned_data['amount']

        if source_account.balance >= amount:
            source_account.balance -= amount
            destination_account.balance += amount
            source_account.save()
            destination_account.save()

            Transaction.objects.create(
                account=source_account,
                amount=-amount,
                description=f'Transferred to {destination_account.account_number}'
            )
            Transaction.objects.create(
                account=destination_account,
                amount=amount,
                description=f'Transferred from {source_account.account_number}'
            )

            messages.success(request, 'Transfer completed successfully!')
        else:
            messages.error(request, 'Insufficient funds in the source account.')

    return redirect('account_dashboard')

@login_required
@require_POST
def deposit_funds(request):
    form = DepositForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']

        account.balance += amount
        account.save()

        Transaction.objects.create(
            account=account,
            amount=amount,
            description='Deposit'
        )

        messages.success(request, 'Deposit completed successfully!')

    return redirect('account_dashboard')

@login_required
@require_POST
def withdraw_funds(request):
    form = WithdrawalForm(request.POST)
    if form.is_valid():
        account = form.cleaned_data['account']
        amount = form.cleaned_data['amount']

        if account.balance >= amount:
            account.balance -= amount
            account.save()

            Transaction.objects.create(
                account=account,
                amount=-amount,
                description='Withdrawal'
            )

            messages.success(request, 'Withdrawal completed successfully!')
        else:
            messages.error(request, 'Insufficient funds in the account.')

    return redirect('account_dashboard')
```