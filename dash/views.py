```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    account = get_object_or_404(Account, user=request.user)

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_management')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    return redirect('account_management')
                else:
                    return HttpResponse("Insufficient funds.")
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                target_account_id = form.cleaned_data['target_account']
                transfer_amount = form.cleaned_data['amount']
                target_account = get_object_or_404(Account, id=target_account_id)
                
                if account.balance >= transfer_amount:
                    account.balance -= transfer_amount
                    target_account.balance += transfer_amount
                    account.save()
                    target_account.save()
                    Transaction.objects.create(account=account, amount=-transfer_amount, transaction_type='Transfer')
                    Transaction.objects.create(account=target_account, amount=transfer_amount, transaction_type='Transfer')
                    return redirect('account_management')
                else:
                    return HttpResponse("Insufficient funds for transfer.")
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]

    return render(request, 'account_management.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    })
```