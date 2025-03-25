```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@csrf_exempt
def bank_operations(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                Account.objects.filter(user=request.user).update(balance=F('balance') + amount)
                Transaction.objects.create(account=request.user.account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'message': 'Deposit successful', 'new_balance': request.user.account.balance})
        
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = request.user.account
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return JsonResponse({'message': 'Withdrawal successful', 'new_balance': account.balance})
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
        
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                target_account = form.cleaned_data['target_account']
                amount = form.cleaned_data['amount']
                sender_account = request.user.account
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    target_account.balance += amount
                    sender_account.save()
                    target_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer', target_account=target_account)
                    return JsonResponse({'message': 'Transfer successful', 'new_balance': sender_account.balance})
                return JsonResponse({'error': 'Insufficient funds'}, status=400)
    
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    context = {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'balance': request.user.account.balance
    }
    
    return render(request, 'bank_operations.html', context)
```