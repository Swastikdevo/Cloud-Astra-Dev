```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def bank_management_view(request):
    user = request.user
    
    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_account = transfer_form.cleaned_data['recipient_account']
                if user.account.balance >= amount:
                    user.account.balance -= amount
                    recipient_account.balance += amount
                    user.account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user.account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Received', sender=user.account)
                    return JsonResponse({'success': True, 'message': 'Transfer successful'})
                else:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds'})
        
        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user.account.balance += amount
                user.account.save()
                Transaction.objects.create(account=user.account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'message': 'Deposit successful'})

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if user.account.balance >= amount:
                    user.account.balance -= amount
                    user.account.save()
                    Transaction.objects.create(account=user.account, amount=-amount, transaction_type='Withdrawal')
                    return JsonResponse({'success': True, 'message': 'Withdrawal successful'})
                else:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds'})

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    transactions = Transaction.objects.filter(account=user.account).order_by('-timestamp')
    return render(request, 'bank_management.html', {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    })
```