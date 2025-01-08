```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Account, Transaction
from .forms import TransferForm, DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    user = request.user
    account = Account.objects.get(user=user)
    
    if request.method == 'POST':
        if 'transfer' in request.POST:
            form = TransferForm(request.POST)
            if form.is_valid():
                recipient_account_number = form.cleaned_data['recipient_account_number']
                amount = form.cleaned_data['amount']
                
                # Handle transfer logic
                recipient_account = Account.objects.get(account_number=recipient_account_number)
                if account.balance >= amount:
                    account.balance -= amount
                    recipient_account.balance += amount
                    account.save()
                    recipient_account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='transfer', recipient=recipient_account)
                    return JsonResponse({'message': 'Transfer successful!'}, status=200)
                else:
                    return JsonResponse({'error': 'Insufficient funds!'}, status=400)

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'message': 'Deposit successful!'}, status=200)

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful!'}, status=200)
                else:
                    return JsonResponse({'error': 'Insufficient funds!'}, status=400)

    else:
        transfer_form = TransferForm()
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'manage_account.html', {
        'account': account,
        'transfer_form': transfer_form,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
    })
```