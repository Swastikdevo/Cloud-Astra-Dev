```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_management(request):
    if request.method == 'POST':
        # Handling deposit
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)
        transfer_form = TransferForm(request.POST)

        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('bank_management')

        elif withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return redirect('bank_management')
            else:
                return HttpResponse("Insufficient balance", status=400)

        elif transfer_form.is_valid():
            target_account_id = transfer_form.cleaned_data['target_account_id']
            amount = transfer_form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            target_account = Account.objects.get(id=target_account_id)

            if account.balance >= amount:
                account.balance -= amount
                target_account.balance += amount
                account.save()
                target_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer to ' + target_account.user.username)
                return redirect('bank_management')
            else:
                return HttpResponse("Insufficient balance", status=400)

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'bank_management.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    })
```