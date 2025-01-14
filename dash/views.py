```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawForm
from django.db import transaction

@login_required
def account_overview(request):
    user_accounts = Account.objects.filter(owner=request.user)
    recent_transactions = Transaction.objects.filter(account__in=user_accounts).order_by('-date')[:5]

    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                with transaction.atomic():
                    # Handle fund transfer logic here
                    sender = form.cleaned_data['sender_account']
                    receiver = form.cleaned_data['receiver_account']
                    amount = form.cleaned_data['amount']
                    if sender.balance >= amount:
                        sender.balance -= amount
                        receiver.balance += amount
                        sender.save()
                        receiver.save()
                        Transaction.objects.create(account=sender, amount=-amount, type='transfer')
                        Transaction.objects.create(account=receiver, amount=amount, type='transfer')
                        return JsonResponse({'success': True, 'message': 'Transfer successful!'})
                    else:
                        return JsonResponse({'success': False, 'message': 'Insufficient funds.'})
        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, type='deposit')
                return JsonResponse({'success': True, 'message': 'Deposit successful!'})
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, type='withdraw')
                    return JsonResponse({'success': True, 'message': 'Withdrawal successful!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds.'})

    # Initialize forms for rendering
    transfer_form = TransferForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    context = {
        'accounts': user_accounts,
        'recent_transactions': recent_transactions,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'bank/account_overview.html', context)
```