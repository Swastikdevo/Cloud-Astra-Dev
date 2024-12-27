```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
def bank_dashboard(request):
    accounts = Account.objects.filter(user=request.user)
    if request.method == "POST":
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                account.balance += amount
                account.save()
                return redirect('bank_dashboard')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                account = withdrawal_form.cleaned_data['account']
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    account.balance -= amount
                    account.save()
                    return redirect('bank_dashboard')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                source_account = transfer_form.cleaned_data['source_account']
                target_account = transfer_form.cleaned_data['target_account']
                amount = transfer_form.cleaned_data['amount']
                if source_account.balance >= amount:
                    Transaction.objects.create(account=source_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer_in')
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    return redirect('bank_dashboard')
                else:
                    return JsonResponse({'error': 'Insufficient funds for transfer'}, status=400)

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    return render(request, 'bank/dashboard.html', {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })
```