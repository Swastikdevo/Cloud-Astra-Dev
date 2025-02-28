```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=user_account).order_by('-date')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='Deposit')
                return redirect('manage_account')

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Withdraw')
                    return redirect('manage_account')
                else:
                    return render(request, 'manage_account.html', {'account': user_account, 'transactions': transactions, 'error': 'Insufficient funds'})

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                if user_account.balance >= amount:
                    try:
                        recipient_account = Account.objects.get(user__username=recipient_username)
                    except Account.DoesNotExist:
                        return render(request, 'manage_account.html', {'account': user_account, 'transactions': transactions, 'error': 'Recipient not found'})

                    user_account.balance -= amount
                    recipient_account.balance += amount
                    user_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=user_account, amount=-amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                    return redirect('manage_account')
                else:
                    return render(request, 'manage_account.html', {'account': user_account, 'transactions': transactions, 'error': 'Insufficient funds'})

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    context = {
        'account': user_account,
        'transactions': transactions,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'manage_account.html', context)
```