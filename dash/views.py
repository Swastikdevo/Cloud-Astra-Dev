```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == "POST":
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'message': 'Deposit successful!'})
        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds!'})
                account.balance -= amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                return JsonResponse({'success': True, 'message': 'Withdrawal successful!'})
        elif 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account = form.cleaned_data['recipient_account']
                amount = form.cleaned_data['amount']
                if amount > account.balance:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds!'})
                account.balance -= amount
                account.save()
                recipient_account.balance += amount
                recipient_account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Transfer', recipient=recipient_account)
                return JsonResponse({'success': True, 'message': 'Transfer successful!'})

    context = {
        'account': account,
        'deposit_form': DepositForm(),
        'withdraw_form': WithdrawForm(),
        'transfer_form': TransferForm(),
    }
    return render(request, 'manage_account.html', context)
```