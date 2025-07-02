```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@csrf_exempt
@login_required
def bank_management_view(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, f'Deposit successful! New balance: ${account.balance}')
                return redirect('bank_management')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, f'Withdrawal successful! New balance: ${account.balance}')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_management')
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                target_user = form.cleaned_data['target_user']
                account = Account.objects.get(user=request.user)
                target_account = Account.objects.get(user__username=target_user)
                
                if amount <= account.balance:
                    account.balance -= amount
                    target_account.balance += amount
                    account.save()
                    target_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer to {}'.format(target_user))
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer from {}'.format(request.user.username))
                    messages.success(request, f'Transfer successful! New balance: ${account.balance}')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_management')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawalForm()
        transfer_form = TransferForm()

    return render(request, 'bank_management.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    })
```