```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST) if 'deposit' in request.POST else None
        withdraw_form = WithdrawForm(request.POST) if 'withdraw' in request.POST else None
        
        if deposit_form and deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return redirect('account_overview')

        elif withdraw_form and withdraw_form.is_valid():
            amount = withdraw_form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                return redirect('account_overview')
            else:
                return JsonResponse({'error': 'Insufficient balance'}, status=400)

    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    
    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transactions': Transaction.objects.filter(account=account).order_by('-date'),
    }
    return render(request, 'bank/account_overview.html', context)
```