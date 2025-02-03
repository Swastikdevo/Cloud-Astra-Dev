```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_overview')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return redirect('account_overview')

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient_username']
                amount = form.cleaned_data['amount']
                recipient_account = Account.objects.get(user__username=recipient_username)
                if amount > account.balance:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
                account.balance -= amount
                recipient_account.balance += amount
                account.save()
                recipient_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer', recipient=recipient_account)
                return redirect('account_overview')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()
    
    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'account_overview.html', context)
```