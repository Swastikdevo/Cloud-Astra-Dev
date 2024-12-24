```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender_account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(account_number=transfer_form.cleaned_data['recipient_account'])
                amount = transfer_form.cleaned_data['amount']
                
                if sender_account.balance >= amount:
                    Transaction.objects.create(
                        from_account=sender_account,
                        to_account=recipient_account,
                        amount=amount,
                        transaction_type='Transfer'
                    )
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = Account.objects.get(user=request.user)
                amount = deposit_form.cleaned_data['amount']
                
                Transaction.objects.create(
                    to_account=account,
                    amount=amount,
                    transaction_type='Deposit'
                )
                account.balance += amount
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                account = Account.objects.get(user=request.user)
                amount = withdrawal_form.cleaned_data['amount']
                
                if account.balance >= amount:
                    Transaction.objects.create(
                        from_account=account,
                        amount=amount,
                        transaction_type='Withdrawal'
                    )
                    account.balance -= amount
                    account.save()
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'account': Account.objects.get(user=request.user)
    }
    
    return render(request, 'bank/manage_account.html', context)
```