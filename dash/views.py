```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@csrf_exempt
@login_required
def bank_management_view(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = request.user.account
                receiver_account = Account.objects.get(id=form.cleaned_data['receiver_account_id'])
                amount = form.cleaned_data['amount']
                if sender_account.balance >= amount:
                    Transaction.objects.create(
                        account=sender_account,
                        amount=-amount,
                        transaction_type='transfer',
                        description=f'Transferred {amount} to {receiver_account.user.username}'
                    )
                    Transaction.objects.create(
                        account=receiver_account,
                        amount=amount,
                        transaction_type='transfer',
                        description=f'Received {amount} from {sender_account.user.username}'
                    )
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful.'})

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = request.user.account
                amount = form.cleaned_data['amount']
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='deposit',
                    description='Deposited funds'
                )
                account.balance += amount
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = request.user.account
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(
                        account=account,
                        amount=-amount,
                        transaction_type='withdrawal',
                        description='Withdrew funds'
                    )
                    account.balance -= amount
                    account.save()
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'})
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
    
    accounts = Account.objects.all()
    return render(request, 'bank/bank_management.html', {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'accounts': accounts,
    })
```