```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_management_view(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                account.balance += amount
                account.save()
                messages.success(request, f'${amount} deposited to your account.')
                return redirect('bank_management')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    messages.success(request, f'${amount} withdrawn from your account.')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_management')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    messages.success(request, f'${amount} transferred from {from_account.account_number} to {to_account.account_number}.')
                else:
                    messages.error(request, 'Insufficient funds for transfer.')
                return redirect('bank_management')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    context = {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form
    }
    
    return render(request, 'bank_management.html', context)
```