```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_overview(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                transaction = Transaction(account=user_account, amount=amount, transaction_type='Deposit')
                transaction.save()
                return redirect('account_overview')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()
                    transaction = Transaction(account=user_account, amount=-amount, transaction_type='Withdrawal')
                    transaction.save()
                    return redirect('account_overview')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
    
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    context = {
        'account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    return render(request, 'account/overview.html', context)
```