```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@csrf_exempt
@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                messages.success(request, 'Deposit successful.')
                return redirect('bank_dashboard')
        
        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    messages.success(request, 'Withdrawal successful.')
                else:
                    messages.error(request, 'Insufficient balance.')
                return redirect('bank_dashboard')
        
        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                amount = form.cleaned_data['amount']
                if amount <= from_account.balance:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                    messages.success(request, 'Transfer successful.')
                else:
                    messages.error(request, 'Insufficient balance.')
                return redirect('bank_dashboard')

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()
    
    return render(request, 'bank/dashboard.html', {
        'user_accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })

```