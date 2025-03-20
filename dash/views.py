```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def manage_bank_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, transaction_type='Deposit', amount=amount)
                messages.success(request, 'Deposit successful!')
                return redirect('manage_bank_account')
        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, transaction_type='Withdrawal', amount=amount)
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient balance for withdrawal.')
                return redirect('manage_bank_account')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        account_info = Account.objects.get(user=request.user)
        transactions = Transaction.objects.filter(account=account_info).order_by('-date')

    context = {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'account_info': account_info,
        'transactions': transactions,
    }
    return render(request, 'bank/manage_account.html', context)

@login_required
def transaction_history(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'bank/transaction_history.html', {'transactions': transactions})

@login_required
def api_balance(request):
    if request.method == 'GET':
        account = Account.objects.get(user=request.user)
        return JsonResponse({'balance': account.balance})
```