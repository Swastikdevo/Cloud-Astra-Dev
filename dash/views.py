```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = Account.objects.get(account_number=form.cleaned_data['sender_account'])
                recipient_account = Account.objects.get(account_number=form.cleaned_data['recipient_account'])
                amount = form.cleaned_data['amount']
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(
                        sender=sender_account,
                        recipient=recipient_account,
                        amount=amount,
                        transaction_type='Transfer'
                    )
                    return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(account_number=form.cleaned_data['account'])
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Deposit'
                )
                return JsonResponse({'status': 'success', 'message': 'Deposit completed successfully.'})

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(account_number=form.cleaned_data['account'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        amount=amount,
                        transaction_type='Withdrawal'
                    )
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal completed successfully.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
    
    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
    
    context = {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form
    }
    return render(request, 'bank/manage_account.html', context)
```