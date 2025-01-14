```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(user=request.user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = deposit_form.cleaned_data['account']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('bank_dashboard')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                account = withdraw_form.cleaned_data['account']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return redirect('bank_dashboard')
                else:
                    return HttpResponse('Insufficient funds')
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                from_account = transfer_form.cleaned_data['from_account']
                to_account = transfer_form.cleaned_data['to_account']
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer_in')
                    return redirect('bank_dashboard')
                else:
                    return HttpResponse('Insufficient funds for transfer')
    
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    context = {
        'accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'bank/dashboard.html', context)
```