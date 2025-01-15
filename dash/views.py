```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_account = form.cleaned_data['recipient_account']
                account = Account.objects.get(user=request.user)

                if account.balance >= amount:
                    Transaction.objects.create(
                        sender=account,
                        receiver=recipient_account,
                        amount=amount
                    )
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful'})

                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

        elif request.POST.get('action') == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                deposit_amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += deposit_amount
                account.save()

                Transaction.objects.create(
                    sender=None,
                    receiver=account,
                    amount=deposit_amount
                )
                return JsonResponse({'status': 'success', 'message': 'Deposit successful'})

        elif request.POST.get('action') == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                withdrawal_amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)

                if account.balance >= withdrawal_amount:
                    account.balance -= withdrawal_amount
                    account.save()

                    Transaction.objects.create(
                        sender=account,
                        receiver=None,
                        amount=withdrawal_amount
                    )
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})

                return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    return render(request, 'account_management.html', {
        'transfer_form': TransferForm(),
        'deposit_form': DepositForm(),
        'withdrawal_form': WithdrawalForm(),
        'balance': Account.objects.get(user=request.user).balance
    })
```