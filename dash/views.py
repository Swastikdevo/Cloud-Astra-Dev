```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm
from django.contrib import messages

@login_required
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, f'Deposited ${amount:.2f} successfully!')
                return redirect('manage_account')
        
        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, f'Withdrew ${amount:.2f} successfully!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account')
        
        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_account = form.cleaned_data['recipient_account']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    recipient = Account.objects.get(account_number=recipient_account)
                    recipient.balance += amount
                    account.save()
                    recipient.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='transfer', recipient=recipient)
                    messages.success(request, f'Transferred ${amount:.2f} to account {recipient_account} successfully!')
                else:
                    messages.error(request, 'Insufficient funds!')
                return redirect('manage_account')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()

    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    
    context = {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
        'transactions': transactions,
    }
    
    return render(request, 'manage_account.html', context)
```