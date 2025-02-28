```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('manage_account')
        
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return redirect('manage_account')
                else:
                    return JsonResponse({"error": "Insufficient balance"})

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_username = form.cleaned_data['recipient']
                sender_account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(user__username=recipient_username)
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer', recipient=recipient_account)
                    return redirect('manage_account')
                else:
                    return JsonResponse({"error": "Insufficient balance"})

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()
        transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    
    context = {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
        'balance': Account.objects.get(user=request.user).balance
    }
    return render(request, 'manage_account.html', context)
```