```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def banking_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(pk=form.cleaned_data['account_id'], owner=request.user)
                account.balance += form.cleaned_data['amount']
                account.save()
                Transaction.objects.create(account=account, amount=form.cleaned_data['amount'], transaction_type='deposit')
                return redirect('banking_dashboard')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(pk=form.cleaned_data['account_id'], owner=request.user)
                if account.balance >= form.cleaned_data['amount']:
                    account.balance -= form.cleaned_data['amount']
                    account.save()
                    Transaction.objects.create(account=account, amount=form.cleaned_data['amount'], transaction_type='withdrawal')
                    return redirect('banking_dashboard')
                else:
                    return render(request, 'banking/dashboard.html', {'error': 'Insufficient funds.', 'accounts': user_accounts})

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = Account.objects.get(pk=form.cleaned_data['from_account_id'], owner=request.user)
                to_account = Account.objects.get(pk=form.cleaned_data['to_account_id'])
                if from_account.balance >= form.cleaned_data['amount']:
                    from_account.balance -= form.cleaned_data['amount']
                    to_account.balance += form.cleaned_data['amount']
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=form.cleaned_data['amount'], transaction_type='transfer_out')
                    Transaction.objects.create(account=to_account, amount=form.cleaned_data['amount'], transaction_type='transfer_in')
                    return redirect('banking_dashboard')
                else:
                    return render(request, 'banking/dashboard.html', {'error': 'Insufficient funds for transfer.', 'accounts': user_accounts})

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    return render(request, 'banking/dashboard.html', {
        'accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })
```