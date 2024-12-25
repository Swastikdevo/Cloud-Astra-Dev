```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'Deposited: ${amount}. New Balance: ${account.balance}.')
                return redirect('account_management')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, f'Withdrew: ${amount}. New Balance: ${account.balance}.')
                else:
                    messages.warning(request, 'Insufficient balance.')
                return redirect('account_management')

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    return render(request, 'account_management.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })
```