```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.contrib import messages

@login_required
def bank_management_view(request):
    user_account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = Account.objects.get(account_number=form.cleaned_data['recipient_account_number'])
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                    messages.success(request, 'Transfer successful!')
                else:
                    messages.error(request, 'Insufficient balance for transfer.')
        
        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
        
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient balance for withdrawal.')

        return redirect('bank_management_view')
    
    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    transactions = Transaction.objects.filter(account=user_account).order_by('-date')[:10]

    context = {
        'account': user_account,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
    }
    
    return render(request, 'bank_management.html', context)
```