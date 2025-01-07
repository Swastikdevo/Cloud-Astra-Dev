```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='deposit')
                return redirect('account_summary')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='withdrawal')
                    return redirect('account_summary')
                else:
                    form.add_error(None, 'Insufficient funds')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')

    return render(request, 'bank/manage_account.html', {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    })

@require_POST
@login_required
def api_transaction_history(request):
    user_account = Account.objects.get(user=request.user)
    transactions = list(Transaction.objects.filter(account=user_account).values('date', 'amount', 'transaction_type'))
    return JsonResponse(transactions, safe=False)
```