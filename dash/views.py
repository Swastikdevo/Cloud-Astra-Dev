```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, AccountCreationForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')

    context = {
        'accounts': accounts,
        'transactions': transactions,
    }
    return render(request, 'bank/dashboard.html', context)

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            new_account.user = request.user
            new_account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('bank:dashboard')
    else:
        form = AccountCreationForm()

    return render(request, 'bank/create_account.html', {'form': form})

@login_required
def deposit(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            messages.success(request, 'Deposit successful!')
            return redirect('bank:dashboard')
    else:
        form = DepositForm()

    return render(request, 'bank/deposit.html', {'form': form, 'account': account})

@login_required
def withdraw(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                messages.success(request, 'Withdrawal successful!')
                return redirect('bank:dashboard')
            else:
                messages.error(request, 'Insufficient funds.')
    else:
        form = WithdrawalForm()

    return render(request, 'bank/withdraw.html', {'form': form, 'account': account})
```