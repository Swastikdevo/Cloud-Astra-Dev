```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, TransferForm

@login_required
@csrf_exempt
def bank_operations_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/operations.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})

        elif action == 'withdrawal':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
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
                from_account = form.cleaned_data['from_account']
                to_account = form.cleaned_data['to_account']
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
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request type!'})
```