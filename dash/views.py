```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    user_accounts = Account.objects.filter(owner=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, id=form.cleaned_data['account_id'], owner=request.user)
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = get_object_or_404(Account, id=form.cleaned_data['account_id'], owner=request.user)
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                from_account = get_object_or_404(Account, id=form.cleaned_data['from_account_id'], owner=request.user)
                to_account = get_object_or_404(Account, id=form.cleaned_data['to_account_id'])
                amount = form.cleaned_data['amount']
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='Transfer In')
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds for transfer!'})

    deposit_form = DepositForm()
    withdrawal_form = WithdrawalForm()
    transfer_form = TransferForm()

    return render(request, 'account/manage_account.html', {
        'user_accounts': user_accounts,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transfer_form': transfer_form,
    })
```