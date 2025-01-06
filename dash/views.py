```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm


@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    account = Account.objects.get(user=request.user)
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('manage_account')
        
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return redirect('manage_account')
                else:
                    withdraw_form.add_error('amount', 'Insufficient funds.')

    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    total_transactions = transactions.count()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions,
        'total_transactions': total_transactions,
    }
    
    return render(request, 'bank/manage_account.html', context)
```