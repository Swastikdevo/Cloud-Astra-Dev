```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def bank_management_view(request):
    accounts = Account.objects.filter(user=request.user)

    if request.method == 'POST':
        transfer_form = TransferForm(request.POST)
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)

        if transfer_form.is_valid():
            sender_account = transfer_form.cleaned_data['sender_account']
            recipient_account = transfer_form.cleaned_data['recipient_account']
            amount = transfer_form.cleaned_data['amount']
            if sender_account.balance >= amount:
                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()
                Transaction.objects.create(
                    account=sender_account,
                    transaction_type='Transfer',
                    amount=-amount,
                    description=f'Transferred to {recipient_account.account_number}'
                )
                Transaction.objects.create(
                    account=recipient_account,
                    transaction_type='Transfer',
                    amount=amount,
                    description=f'Received from {sender_account.account_number}'
                )
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

        elif deposit_form.is_valid():
            account = deposit_form.cleaned_data['account']
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(
                account=account,
                transaction_type='Deposit',
                amount=amount,
                description='Deposit'
            )
            return JsonResponse({'status': 'success'})

        elif withdrawal_form.is_valid():
            account = withdrawal_form.cleaned_data['account']
            amount = withdrawal_form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    transaction_type='Withdrawal',
                    amount=-amount,
                    description='Withdrawal'
                )
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'accounts': accounts,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    
    return render(request, 'bank_management.html', context)
```