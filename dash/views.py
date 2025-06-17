```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = get_object_or_404(Account, id=request.user.account.id)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('account_detail')
        
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = get_object_or_404(Account, id=request.user.account.id)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return redirect('account_detail')
        
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                receiver_account_id = form.cleaned_data['receiver_account_id']
                sender_account = get_object_or_404(Account, id=request.user.account.id)
                receiver_account = get_object_or_404(Account, id=receiver_account_id)
                
                if amount <= sender_account.balance:
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='transfer_in')
                    return redirect('account_detail')

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()
    
    context = {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'bank/manage_account.html', context)
```