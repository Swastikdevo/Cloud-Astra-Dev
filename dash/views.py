```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_overview(request):
    account = get_object_or_404(Account, user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    context = {
        'account': account,
        'transactions': transactions,
        'deposit_form': DepositForm(),
        'withdrawal_form': WithdrawalForm(),
        'transfer_form': TransferForm(),
    }
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_overview')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return redirect('account_overview')
                else:
                    return JsonResponse({'error': 'Insufficient balance.'}, status=400)
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                amount = transfer_form.cleaned_data['amount']
                recipient_username = transfer_form.cleaned_data['recipient']
                recipient = get_object_or_404(User, username=recipient_username)
                recipient_account = get_object_or_404(Account, user=recipient)

                if amount <= account.balance:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer-Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer-In')
                    return redirect('account_overview')
                else:
                    return JsonResponse({'error': 'Insufficient balance.'}, status=400)

    return render(request, 'bank/account_overview.html', context)
```