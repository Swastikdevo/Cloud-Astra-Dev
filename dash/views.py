```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    user = request.user
    account = Account.objects.get(user=user)

    # Deposit Money
    if request.method == 'POST' and 'deposit' in request.POST:
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('manage_account')
    else:
        deposit_form = DepositForm()

    # Withdraw Money
    if request.method == 'POST' and 'withdraw' in request.POST:
        withdrawal_form = WithdrawalForm(request.POST)
        if withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            if amount > account.balance:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
            account.balance -= amount
            account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
            return redirect('manage_account')
    else:
        withdrawal_form = WithdrawalForm()

    # Transfer Money
    if request.method == 'POST' and 'transfer' in request.POST:
        transfer_form = TransferForm(request.POST)
        if transfer_form.is_valid():
            to_account_number = transfer_form.cleaned_data['to_account_number']
            amount = transfer_form.cleaned_data['amount']
            if amount > account.balance:
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
            recipient_account = Account.objects.get(account_number=to_account_number)
            account.balance -= amount
            recipient_account.balance += amount
            account.save()
            recipient_account.save()
            Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
            Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer', sender=account)
            return redirect('manage_account')
    else:
        transfer_form = TransferForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'manage_account.html', context)
```