```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('account_dashboard')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return redirect('account_dashboard')
                else:
                    error_message = 'Insufficient funds'
                    return render(request, 'account_dashboard.html', {'account': account, 'transactions': transactions, 'withdrawal_form': withdrawal_form, 'deposit_form': deposit_form, 'error': error_message})

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'account_dashboard.html', {
        'account': account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form
    })

@require_POST
@login_required
def ajax_balance_check(request):
    account = Account.objects.get(user=request.user)
    return JsonResponse({'balance': account.balance})
```