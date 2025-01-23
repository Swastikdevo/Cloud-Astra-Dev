```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_view(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'message': 'Deposit successful!', 'balance': account.balance})

        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful!', 'balance': account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient_account'])
                sender_account = Account.objects.get(user=request.user)
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                    return JsonResponse({'message': 'Transfer successful!', 'balance': sender_account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()
    
    context = {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/index.html', context)
```