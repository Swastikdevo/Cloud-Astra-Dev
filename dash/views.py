```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    account = get_object_or_404(Account, user=request.user)

    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = get_object_or_404(Account, account_number=form.cleaned_data['recipient_account'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    
                    # Log transaction
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Received', sender=account)
                    
                    return JsonResponse({'message': 'Transfer successful'})
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                
                # Log transaction
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                
                return JsonResponse({'message': 'Deposit successful'})
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()

                    # Log transaction
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    
                    return JsonResponse({'message': 'Withdrawal successful'})
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    
    return render(request, 'manage_account.html', {
        'account': account,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```