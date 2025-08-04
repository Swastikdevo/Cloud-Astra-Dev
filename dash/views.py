```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_management(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'message': 'Deposit successful', 'balance': account.balance})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return JsonResponse({'message': 'Withdrawal successful', 'balance': account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_username = form.cleaned_data['recipient']
                sender_account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(user__username=recipient_username)
                
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer_out', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in', sender=sender_account)
                    return JsonResponse({'message': 'Transfer successful', 'balance': sender_account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    account = Account.objects.get(user=request.user)

    context = {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'balance': account.balance,
    }
    return render(request, 'bank_management.html', context)
```