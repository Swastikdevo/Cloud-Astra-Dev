```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
def bank_management_view(request):
    user_accounts = Account.objects.filter(owner=request.user)
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = transfer_form.cleaned_data['sender_account']
                receiver_account = transfer_form.cleaned_data['receiver_account']
                amount = transfer_form.cleaned_data['amount']
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='transfer', target_account=receiver_account)
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='transfer', target_account=sender_account)
                    return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit completed successfully.'})
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = withdraw_form.cleaned_data['account']
                amount = withdraw_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdraw')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal completed successfully.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    return render(request, 'bank_management.html', {
        'user_accounts': user_accounts,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```