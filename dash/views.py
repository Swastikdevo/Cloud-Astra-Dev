```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = get_object_or_404(Account, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'message': 'Deposit successful.'})

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = get_object_or_404(Account, user=request.user)
                if amount > account.balance:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds.'})
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                return JsonResponse({'success': True, 'message': 'Withdrawal successful.'})
        
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                sender_account = get_object_or_404(Account, user=request.user)
                recipient_account = get_object_or_404(Account, user__username=recipient_username)
                
                if amount > sender_account.balance:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds for transfer.'})

                sender_account.balance -= amount
                recipient_account.balance += amount
                sender_account.save()
                recipient_account.save()
                Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer to {}'.format(recipient_username))
                Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer from {}'.format(request.user.username))
                return JsonResponse({'success': True, 'message': 'Transfer successful.'})

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()
    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form
    })
```