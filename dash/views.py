```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, 'Deposit successful! Your new balance is ${}'.format(account.balance))
                return redirect('account_overview')
        elif form_type == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds.')
                else:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, 'Withdrawal successful! Your new balance is ${}'.format(account.balance))
                return redirect('account_overview')
        elif form_type == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, 'Insufficient funds.')
                else:
                    try:
                        recipient = Account.objects.get(user__username=recipient_username)
                        account.balance -= amount
                        recipient.balance += amount
                        account.save()
                        recipient.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='transfer', recipient=recipient)
                        messages.success(request, 'Transfer successful! Your new balance is ${}'.format(account.balance))
                    except Account.DoesNotExist:
                        messages.error(request, 'Recipient does not exist.')
                return redirect('account_overview')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'account/overview.html', context)
```