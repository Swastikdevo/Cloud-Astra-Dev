```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def bank_management_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # Deposit
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(pk=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})

        # Withdraw
        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(pk=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})

        # Transfer
        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                source_account = Account.objects.get(pk=form.cleaned_data['source_account_id'])
                target_account = Account.objects.get(pk=form.cleaned_data['target_account_id'])
                amount = form.cleaned_data['amount']
                if source_account.balance >= amount:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(account=source_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer_in')
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})

    else:
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank_management.html', {'accounts': accounts})
```