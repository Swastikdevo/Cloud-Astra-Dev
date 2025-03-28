```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def account_management_view(request):
    """Handle various account management actions including deposits, withdrawals, and transfers."""
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'new_balance': account.balance})
        
        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'new_balance': account.balance})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'}, status=400)

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient_username = form.cleaned_data['recipient']
                try:
                    recipient_account = Account.objects.get(user__username=recipient_username)
                    if amount <= account.balance:
                        account.balance -= amount
                        recipient_account.balance += amount
                        account.save()
                        recipient_account.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='transfer_out', recipient=recipient_account)
                        Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='transfer_in', sender=account)
                        return JsonResponse({'status': 'success', 'new_balance': account.balance})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'}, status=400)
                except Account.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Recipient account does not exist.'}, status=404)

    # If GET request, render account management page
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()
    transfer_form = TransferForm()
    
    return render(request, 'account_management.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
    })
```