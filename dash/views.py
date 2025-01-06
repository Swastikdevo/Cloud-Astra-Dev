```python
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm
from django.contrib.auth.decorators import login_required

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, id=form.cleaned_data['account_id'], owner=request.user)
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, id=form.cleaned_data['account_id'], owner=request.user)
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return JsonResponse({'status': 'success', 'new_balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                sender_account = get_object_or_404(Account, id=form.cleaned_data['sender_id'], owner=request.user)
                receiver_account = get_object_or_404(Account, id=form.cleaned_data['receiver_id'])
                amount = form.cleaned_data['amount']
                if sender_account.balance >= amount:
                    sender_account.balance -= amount
                    receiver_account.balance += amount
                    sender_account.save()
                    receiver_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=receiver_account, amount=amount, transaction_type='transfer_in')
                    return JsonResponse({'status': 'success', 'new_sender_balance': sender_account.balance, 'new_receiver_balance': receiver_account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})

    accounts = Account.objects.filter(owner=request.user)
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    context = {
        'accounts': accounts,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    }
    return render(request, 'bank/manage_account.html', context)
```