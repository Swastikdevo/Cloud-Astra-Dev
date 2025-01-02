```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BankAccount, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = BankAccount.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, "Deposit successful!")
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    messages.error(request, "Insufficient funds!")
                else:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    messages.success(request, "Withdrawal successful!")
                    return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'bank/manage_account.html', {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```