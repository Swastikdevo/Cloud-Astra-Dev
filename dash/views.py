```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        return render(request, 'bank_management.html', {
            'accounts': accounts,
            'transfer_form': transfer_form,
            'deposit_form': deposit_form,
            'withdraw_form': withdraw_form,
        })

    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = form.cleaned_data['from_account']
                receiver_account = form.cleaned_data['to_account']
                amount = form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    Transaction.objects.create(account=sender_account, amount=-amount, transaction_type='Transfer', to_account=receiver_account)
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='Transfer', from_account=sender_account)
                    return JsonResponse({'status': 'success', 'message': 'Transfer completed successfully!'})
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance!'})

        elif action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit completed successfully!'})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal completed successfully!'})
                return JsonResponse({'status': 'error', 'message': 'Insufficient balance!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request!'})
```