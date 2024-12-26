```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = form.cleaned_data['sender_account']
                receiver_account = form.cleaned_data['receiver_account']
                amount = form.cleaned_data['amount']
                if Account.objects.filter(account_number=sender_account).exists() and \
                   Account.objects.filter(account_number=receiver_account).exists():
                    # Execute the transfer
                    sender = Account.objects.get(account_number=sender_account)
                    receiver = Account.objects.get(account_number=receiver_account)
                    if sender.balance >= amount:
                        sender.balance -= amount
                        receiver.balance += amount
                        sender.save()
                        receiver.save()
                        Transaction.objects.create(account=sender, amount=-amount, transaction_type='Transfer')
                        Transaction.objects.create(account=receiver, amount=amount, transaction_type='Transfer')
                        return JsonResponse({'status': 'success', 'message': 'Transfer completed'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
                return JsonResponse({'status': 'error', 'message': 'Invalid account numbers'})

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account_number = form.cleaned_data['account_number']
                amount = form.cleaned_data['amount']
                if Account.objects.filter(account_number=account_number).exists():
                    account = Account.objects.get(account_number=account_number)
                    account.balance += amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                    return JsonResponse({'status': 'success', 'message': 'Deposit completed'})
                return JsonResponse({'status': 'error', 'message': 'Invalid account number'})

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account_number = form.cleaned_data['account_number']
                amount = form.cleaned_data['amount']
                if Account.objects.filter(account_number=account_number).exists():
                    account = Account.objects.get(account_number=account_number)
                    if account.balance >= amount:
                        account.balance -= amount
                        account.save()
                        Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                        return JsonResponse({'status': 'success', 'message': 'Withdrawal completed'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
                return JsonResponse({'status': 'error', 'message': 'Invalid account number'})
    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
    
    context = {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'bank_management.html', context)
```