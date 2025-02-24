```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST) if 'deposit' in request.POST else WithdrawalForm(request.POST)
        
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            if 'deposit' in request.POST:
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                return redirect('account_dashboard')
            elif 'withdraw' in request.POST and amount <= user_account.balance:
                user_account.balance -= amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Withdrawal')
                return redirect('account_dashboard')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    
    context = {
        'account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    
    return render(request, 'account/dashboard.html', context)

@login_required
def transaction_history(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    return render(request, 'account/transaction_history.html', {'transactions': transactions})

@login_required
def account_summary(request):
    user_account = Account.objects.get(user=request.user)
    return JsonResponse({
        'account_number': user_account.account_number,
        'balance': user_account.balance,
        'owner': user_account.user.username
    })
```