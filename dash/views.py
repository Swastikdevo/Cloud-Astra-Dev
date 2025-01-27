```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__in=accounts).order_by('-date')[:10]

    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                transfer_form.save()
                return redirect('bank_dashboard')

        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                deposit_form.save()
                return redirect('bank_dashboard')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                withdrawal_form.save()
                return redirect('bank_dashboard')
    
    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }
    
    return render(request, 'bank/dashboard.html', context)

@login_required
def fetch_account_balance(request, account_id):
    account = Account.objects.filter(id=account_id, user=request.user).first()
    if account:
        return JsonResponse({'balance': account.balance})
    return JsonResponse({'error': 'Account not found.'}, status=404)
```