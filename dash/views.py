```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def bank_view(request):
    accounts = Account.objects.filter(user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(
                        from_account=from_account,
                        to_account=to_account,
                        amount=amount,
                        transaction_type='transfer'
                    )
                    messages.success(request, 'Transfer completed successfully.')
                else:
                    messages.error(request, 'Insufficient funds for this transfer.')
        
        elif action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='deposit'
                )
                messages.success(request, 'Deposit successful.')

        elif action == 'withdrawal':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(
                        account=account,
                        amount=amount,
                        transaction_type='withdrawal'
                    )
                    messages.success(request, 'Withdrawal successful.')
                else:
                    messages.error(request, 'Insufficient funds for this withdrawal.')
        
        return redirect('bank_view')

    context = {
        'accounts': accounts,
        'transfer_form': TransferForm(),
        'deposit_form': DepositForm(),
        'withdrawal_form': WithdrawalForm(),
    }
    
    return render(request, 'bank/bank_view.html', context)
```