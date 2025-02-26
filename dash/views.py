```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.core.exceptions import PermissionDenied

@login_required
def account_view(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        if 'perform_transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = form.cleaned_data['recipient_account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    # Perform the transfer
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='transfer', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer', sender=account)
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})
        elif 'perform_deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})
        elif 'perform_withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdraw')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})
    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
    
    context = {
        'account': account,
        'transactions': transactions,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'bank/account.html', context)
```