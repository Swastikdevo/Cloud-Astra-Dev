```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def manage_account(request):
    user_accounts = Account.objects.filter(owner=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = form.cleaned_data['sender_account']
                recipient_account = form.cleaned_data['recipient_account']
                amount = form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()

                    Transaction.objects.create(
                        account=sender_account,
                        amount=-amount,
                        transaction_type='Transfer to ' + recipient_account.account_number
                    )
                    Transaction.objects.create(
                        account=recipient_account,
                        amount=amount,
                        transaction_type='Transfer from ' + sender_account.account_number
                    )
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

        elif action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                
                account.balance += amount
                account.save()
                
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='Deposit'
                )
                return JsonResponse({'status': 'success', 'message': 'Deposit successful'})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    
                    Transaction.objects.create(
                        account=account,
                        amount=-amount,
                        transaction_type='Withdrawal'
                    )
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    context = {
        'user_accounts': user_accounts,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'bank/manage_account.html', context)
```