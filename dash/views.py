```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_management(request):
    if request.method == "POST":
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_account = transfer_form.cleaned_data['recipient_account']
                sender_account = Account.objects.get(user=request.user)
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(sender=sender_account, recipient=recipient_account, amount=amount, transaction_type='transfer')
                    return JsonResponse({'message': 'Transfer successful!', 'balance': sender_account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds!'}, status=400)

        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'message': 'Deposit successful!', 'balance': account.balance})

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful!', 'balance': account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds!'}, status=400)

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'bank_management.html', {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```