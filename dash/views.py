```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def bank_operations(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient_account'])
                amount = transfer_form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    # Create transaction for sender
                    Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='Transfer')
                    # Create transaction for recipient
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer')
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    return JsonResponse({'message': 'Transfer successful!'}, status=200)
                else:
                    return JsonResponse({'error': 'Insufficient funds!'}, status=400)

        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = Account.objects.get(user=request.user)
                amount = deposit_form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                account.balance += amount
                account.save()
                return JsonResponse({'message': 'Deposit successful!'}, status=200)

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = Account.objects.get(user=request.user)
                amount = withdraw_form.cleaned_data['amount']
                
                if account.balance >= amount:
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    account.balance -= amount
                    account.save()
                    return JsonResponse({'message': 'Withdrawal successful!'}, status=200)
                else:
                    return JsonResponse({'error': 'Insufficient funds!'}, status=400)

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    return render(request, 'bank_operations.html', {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```