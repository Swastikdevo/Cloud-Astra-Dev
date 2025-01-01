```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def account_dashboard(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

@require_POST
@login_required
def transfer_funds(request):
    form = TransferForm(request.POST)
    if form.is_valid():
        sender_account = form.cleaned_data['sender_account']
        receiver_account = form.cleaned_data['receiver_account']
        amount = form.cleaned_data['amount']

        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()

            Transaction.objects.create(
                account=sender_account,
                amount=-amount,
                transaction_type='Transfer Out'
            )
            Transaction.objects.create(
                account=receiver_account,
                amount=amount,
                transaction_type='Transfer In'
            )
            return JsonResponse({'success': True, 'message': 'Transfer completed successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Insufficient funds.'})

    return JsonResponse({'success': False, 'message': 'Invalid data.'})

@login_required
def deposit_funds(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()

            Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='Deposit'
            )
            return redirect('account_dashboard')

    else:
        form = DepositForm()

    return render(request, 'bank/deposit_funds.html', {'form': form})

@login_required
def withdraw_funds(request):
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']

            if account.balance >= amount:
                account.balance -= amount
                account.save()

                Transaction.objects.create(
                    account=account,
                    amount=-amount,
                    transaction_type='Withdrawal'
                )
                return redirect('account_dashboard')
            else:
                form.add_error('amount', 'Insufficient funds.')

    else:
        form = WithdrawalForm()

    return render(request, 'bank/withdraw_funds.html', {'form': form})
```