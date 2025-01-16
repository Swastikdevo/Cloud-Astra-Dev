```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@csrf_exempt
def bank_management_view(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                return redirect('bank_management_view')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Withdraw')
                    return redirect('bank_management_view')
                else:
                    return HttpResponse("Insufficient funds.")
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    if user_account.balance >= amount:
                        user_account.balance -= amount
                        recipient_account.balance += amount
                        user_account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Transfer', recipient=recipient_account)
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer', sender=user_account)
                        return redirect('bank_management_view')
                    else:
                        return HttpResponse("Insufficient funds.")
                except Account.DoesNotExist:
                    return HttpResponse("Recipient account does not exist.")

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()

    context = {
        'user_account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank_management.html', context)
```