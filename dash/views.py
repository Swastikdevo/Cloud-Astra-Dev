```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@require_http_methods(['GET', 'POST'])
def account_management_view(request):
    user_accounts = Account.objects.filter(owner=request.user)

    if request.method == 'POST':
        if 'transfer' in request.POST:
            transfer_form = TransferForm(request.POST)
            if transfer_form.is_valid():
                sender = transfer_form.cleaned_data['sender']
                recipient = transfer_form.cleaned_data['recipient']
                amount = transfer_form.cleaned_data['amount']

                if sender.balance >= amount:
                    sender.balance -= amount
                    recipient.balance += amount
                    sender.save()
                    recipient.save()
                    Transaction.objects.create(account=sender, amount=-amount, transaction_type='transfer')
                    Transaction.objects.create(account=recipient, amount=amount, transaction_type='transfer')
                    return redirect('account_management')
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

        elif 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                account = deposit_form.cleaned_data['account']
                amount = deposit_form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('account_management')

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                account = withdrawal_form.cleaned_data['account']
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                    return redirect('account_management')
                else:
                    return JsonResponse({'error': 'Insufficient funds.'}, status=400)

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    context = {
        'user_accounts': user_accounts,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    }

    return render(request, 'bank/account_management.html', context)
```