```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@method_decorator(login_required, name='dispatch')
def account_overview(request):
    user = request.user
    account = Account.objects.get(user=user)
    
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
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdraw')
                    return redirect('account_overview')
                else:
                    form.add_error(None, "Insufficient funds")

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    return render(request, 'account/overview.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': transactions
    })


@csrf_exempt
@login_required
def transaction_history(request):
    user = request.user
    account = Account.objects.get(user=user)
    transactions = Transaction.objects.filter(account=account).values('created_at', 'amount', 'transaction_type').order_by('-created_at')
    
    return JsonResponse(list(transactions), safe=False)
```