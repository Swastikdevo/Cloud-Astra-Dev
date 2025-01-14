```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        # Handling deposit
        deposit_form = DepositForm(request.POST)
        withdraw_form = WithdrawForm(request.POST)
        transfer_form = TransferForm(request.POST)

        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return JsonResponse({'status': 'success', 'message': 'Deposit successful!', 'balance': account.balance})

        elif withdraw_form.is_valid():
            amount = withdraw_form.cleaned_data['amount']
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!', 'balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})

        elif transfer_form.is_valid():
            recipient_username = transfer_form.cleaned_data['recipient_username']
            amount = transfer_form.cleaned_data['amount']
            if account.balance >= amount:
                recipient_account = Account.objects.get(user__username=recipient_username)
                account.balance -= amount
                recipient_account.balance += amount
                account.save()
                recipient_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                return JsonResponse({'status': 'success', 'message': 'Transfer successful!', 'balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds for transfer!'})

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'manage_account.html', context)
```