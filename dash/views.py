```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def banking_operations(request):
    if request.method == "POST":
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender = request.user
                receiver_account = transfer_form.cleaned_data['receiver']
                amount = transfer_form.cleaned_data['amount']

                if sender.balance >= amount:
                    sender.balance -= amount
                    receiver_account.balance += amount
                    sender.save()
                    receiver_account.save()

                    Transaction.objects.create(account=sender, amount=-amount, transaction_type='Transfer')
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='Transfer')

                    return JsonResponse({'status': 'success', 'message': 'Transfer successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']

                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')

                return JsonResponse({'status': 'success', 'message': 'Deposit successful'})
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                account = withdrawal_form.cleaned_data['account']
                amount = withdrawal_form.cleaned_data['amount']

                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')

                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance'})
    
    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    
    context = {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    return render(request, 'banking_operations.html', context)
```