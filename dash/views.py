```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
def manage_account(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return redirect('account_detail')

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
                return redirect('account_detail')

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_username = form.cleaned_data['recipient']
                amount = form.cleaned_data['amount']
                sender_account = Account.objects.get(user=request.user)
                recipient_account = Account.objects.get(user__username=recipient_username)

                if amount <= sender_account.balance:
                    sender_account.balance -= amount
                    recipient_account.balance += amount
                    sender_account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=sender_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=recipient_account, amount=amount, transaction_type='Transfer In')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
                return redirect('account_detail')
    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        transfer_form = TransferForm()

    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    
    return render(request, 'account/manage_account.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'transfer_form': transfer_form,
        'account': account,
        'transactions': transactions,
    })
```