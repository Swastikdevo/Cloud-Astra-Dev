```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('bank_dashboard')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                account = withdraw_form.cleaned_data['account']
                amount = withdraw_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('bank_dashboard')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = transfer_form.cleaned_data['sender_account']
                receiver_account = transfer_form.cleaned_data['receiver_account']
                amount = transfer_form.cleaned_data['amount']
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='Transfer In')
                    return redirect('bank_dashboard')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    context = {
        'accounts': user_accounts,
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
        'transfer_form': TransferForm(),
    }

    return render(request, 'bank/dashboard.html', context)
```