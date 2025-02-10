```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, AccountCreationForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful!')
                return redirect('manage_account')
        elif 'withdrawal' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account')
    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        account = Account.objects.get(user=request.user)
    
    transactions = Transaction.objects.filter(account=account).order_by('-date')[:10]
    
    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'account': account,
        'transactions': transactions,
    })

@login_required
def account_summary(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account)
    total_deposits = transactions.filter(transaction_type='Deposit').aggregate(Sum('amount'))['amount__sum'] or 0
    total_withdrawals = transactions.filter(transaction_type='Withdrawal').aggregate(Sum('amount'))['amount__sum'] or 0

    return JsonResponse({
        'account_number': account.account_number,
        'balance': account.balance,
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
    })

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
    else:
        form = AccountCreationForm()
    
    return render(request, 'create_account.html', {'form': form})
```