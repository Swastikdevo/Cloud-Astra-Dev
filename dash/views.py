```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    account = get_object_or_404(Account, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "deposit":
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_dashboard')

        elif action == "withdraw":
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('account_dashboard')
                else:
                    form.add_error(None, "Insufficient balance")

        elif action == "transfer":
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = get_object_or_404(Account, account_number=form.cleaned_data['recipient_account_number'])
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                    return redirect('account_dashboard')
                else:
                    form.add_error(None, "Insufficient balance")
        else:
            form = None

    else:
        form = None

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdrawal_form': WithdrawalForm(),
        'transfer_form': TransferForm(),
    }

    return render(request, 'bank/account_dashboard.html', context)
```