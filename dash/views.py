```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def account_view(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_view')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    return redirect('account_view')
                else:
                    return render(request, 'account/view.html', {
                        'account': account,
                        'transactions': transactions,
                        'error': 'Insufficient funds'
                    })

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    
    return render(request, 'account/view.html', {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```