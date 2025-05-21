```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transfer_form = TransferForm()
        return render(request, 'bank_management.html', {
            'accounts': accounts,
            'deposit_form': deposit_form,
            'withdrawal_form': withdrawal_form,
            'transfer_form': transfer_form
        })
    
    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = form.cleaned_data['account']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='transfer_out')
                    Transaction.objects.create(account=to_account, amount=amount, transaction_type='transfer_in')
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds for transfer!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
```