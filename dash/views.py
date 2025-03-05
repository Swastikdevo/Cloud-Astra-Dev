```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'new_balance': user_account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'success': True, 'new_balance': user_account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient funds'})

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                target_account_number = form.cleaned_data['target_account_number']
                transfer_amount = form.cleaned_data['amount']
                if transfer_amount <= user_account.balance:
                    target_account = Account.objects.get(account_number=target_account_number)
                    user_account.balance -= transfer_amount
                    target_account.balance += transfer_amount
                    user_account.save()
                    target_account.save()
                    Transaction.objects.create(account=user_account, amount=transfer_amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=transfer_amount, transaction_type='Transfer In')
                    return JsonResponse({'success': True, 'new_balance': user_account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient funds'})

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    return render(request, 'bank/manage_account.html', {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })
```