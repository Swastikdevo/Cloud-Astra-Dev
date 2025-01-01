```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm
from django.contrib import messages

@login_required
@csrf_exempt
def bank_operations(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                sender = request.user.account
                receiver_account_number = form.cleaned_data['receiver_account_number']
                amount = form.cleaned_data['amount']
                
                try:
                    receiver = Account.objects.get(account_number=receiver_account_number)
                    Transaction.objects.create(sender=sender, receiver=receiver, amount=amount, transaction_type='transfer')
                    messages.success(request, 'Transfer successful.')
                    return redirect('bank_home')
                except Account.DoesNotExist:
                    messages.error(request, 'Receiver account does not exist.')
        
        elif request.POST.get('action') == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = request.user.account
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, 'Deposit successful.')
                return redirect('bank_home')
        
        elif request.POST.get('action') == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = request.user.account
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    messages.success(request, 'Withdrawal successful.')
                else:
                    messages.error(request, 'Insufficient funds.')
                return redirect('bank_home')

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'bank_operations.html', {
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```