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
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()
                Transaction.objects.create(account=user_account, amount=amount, transaction_type='deposit')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    user_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='withdraw')
                    return redirect('manage_account')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
        elif 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                target_account = transfer_form.cleaned_data['target_account']
                amount = transfer_form.cleaned_data['amount']
                if user_account.balance >= amount:
                    user_account.balance -= amount
                    target_account.balance += amount
                    user_account.save()
                    target_account.save()
                    Transaction.objects.create(account=user_account, amount=amount, transaction_type='transfer', target_account=target_account)
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='transfer', source_account=user_account)
                    return redirect('manage_account')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

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
    return render(request, 'bank/manage_account.html', context)
```