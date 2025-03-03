```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm

@login_required
def bank_dashboard(request):
    user_accounts = Account.objects.filter(owner=request.user)
    context = {
        'accounts': user_accounts,
        'total_balance': sum(account.balance for account in user_accounts),
    }
    return render(request, 'bank/dashboard.html', context)

@login_required
def transfer_funds(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            source_account = form.cleaned_data['source_account']
            destination_account = form.cleaned_data['destination_account']

            if source_account.balance >= amount:
                source_account.balance -= amount
                destination_account.balance += amount
                source_account.save()
                destination_account.save()

                Transaction.objects.create(
                    account=source_account,
                    amount=-amount,
                    transaction_type='Transfer',
                    description=f'Transferred to {destination_account.account_number}'
                )
                Transaction.objects.create(
                    account=destination_account,
                    amount=amount,
                    transaction_type='Transfer',
                    description=f'Received from {source_account.account_number}'
                )

                return JsonResponse({'status': 'success', 'message': 'Transfer completed!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'})
    else:
        form = TransferForm()

    return render(request, 'bank/transfer.html', {'form': form})

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(account__owner=request.user).order_by('-date')
    return render(request, 'bank/transactions.html', {'transactions': transactions})
```