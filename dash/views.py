```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_overview.html', {'accounts': user_accounts})

@login_required
@require_POST
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        source_account = form.cleaned_data['source_account']
        target_account = form.cleaned_data['target_account']
        amount = form.cleaned_data['amount']

        if source_account.balance >= amount:
            source_account.balance -= amount
            target_account.balance += amount
            source_account.save()
            target_account.save()

            Transaction.objects.create(
                account=source_account,
                amount=-amount,
                description=f'Transferred to {target_account.account_number}'
            )
            Transaction.objects.create(
                account=target_account,
                amount=amount,
                description=f'Transferred from {source_account.account_number}'
            )
            return redirect('account_overview')
        else:
            return HttpResponse("Insufficient funds.", status=400)

    return render(request, 'bank/transfer_funds.html', {'form': form})

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
        return redirect('account_overview')

    return render(request, 'bank/deposit_funds.html', {'form': form})

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
            return redirect('account_overview')
        else:
            return HttpResponse("Insufficient funds.", status=400)

    return render(request, 'bank/withdraw_funds.html', {'form': form})
```