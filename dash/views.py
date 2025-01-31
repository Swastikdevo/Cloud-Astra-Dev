```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_account = transfer_form.cleaned_data['recipient_account']
                account = Account.objects.get(user=request.user)

                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, type='Transfer', recipient=recipient_account)
                    return JsonResponse({'message': 'Transfer successful', 'balance': account.balance}, status=200)
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
        
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, type='Deposit')
                return JsonResponse({'message': 'Deposit successful', 'balance': account.balance}, status=200)

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)

                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, type='Withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful', 'balance': account.balance}, status=200)
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    context = {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'account': Account.objects.get(user=request.user)
    }
    return render(request, 'bank/manage_account.html', context)
```