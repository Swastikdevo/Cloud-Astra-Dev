```python
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def bank_management(request):
    user = request.user
    accounts = Account.objects.filter(owner=user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.deposit(amount)
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('bank_management')
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.withdraw(amount)
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                return redirect('bank_management')
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                amount = form.cleaned_data['amount']
                from_account.transfer(to_account, amount)
                Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                return redirect('bank_management')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    
    return render(request, 'bank_management.html', context)
```