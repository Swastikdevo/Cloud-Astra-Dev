```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_view(request, account_id):
    account = get_object_or_404(Account, id=account_id, owner=request.user)

    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = get_object_or_404(Account, account_number=form.cleaned_data['recipient_account_number'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    
                    Transaction.objects.create(account=account, type='transfer', amount=amount, recipient=recipient_account)
                    return redirect('account_detail', account_id=account.id)
                else:
                    return HttpResponse("Insufficient funds.", status=400)
        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                
                Transaction.objects.create(account=account, type='deposit', amount=amount)
                return redirect('account_detail', account_id=account.id)
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    
                    Transaction.objects.create(account=account, type='withdrawal', amount=amount)
                    return redirect('account_detail', account_id=account.id)
                else:
                    return HttpResponse("Insufficient funds.", status=400)
    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'account': account,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    
    return render(request, 'account_detail.html', context)
```