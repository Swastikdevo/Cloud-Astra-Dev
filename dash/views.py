```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def account_overview(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    return render(request, 'bank/account_overview.html', {
        'account': account,
        'transactions': transactions,
    })

@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()
            
            Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
            return JsonResponse({'status': 'success', 'balance': account.balance})

    else:
        form = DepositForm()
    
    return render(request, 'bank/deposit.html', {'form': form})

@login_required
def withdrawal(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            account = Account.objects.get(user=request.user)
            
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return JsonResponse({'status': 'success', 'balance': account.balance})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
    
    else:
        form = WithdrawalForm()
    
    return render(request, 'bank/withdrawal.html', {'form': form})

@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_username = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            sender_account = Account.objects.get(user=request.user)

            if sender_account.balance >= amount:
                recipient_account = Account.objects.get(user__username=recipient_username)
                sender_account.balance -= amount
                recipient_account.balance += amount

                sender_account.save()
                recipient_account.save()
                Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
                Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                
                return JsonResponse({'status': 'success', 'balance': sender_account.balance})

            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    else:
        form = TransferForm()

    return render(request, 'bank/transfer.html', {'form': form})
```