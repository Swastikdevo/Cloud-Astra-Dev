```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, TransferForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/accounts.html', {'accounts': accounts})
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account_id = form.cleaned_data['account']
                account = Account.objects.get(id=account_id)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'})

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account_id = form.cleaned_data['account']
                account = Account.objects.get(id=account_id)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return JsonResponse({'status': 'success', 'message': 'Withdraw successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'})

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                from_account_id = form.cleaned_data['from_account']
                to_account_id = form.cleaned_data['to_account']
                from_account = Account.objects.get(id=from_account_id)
                to_account = Account.objects.get(id=to_account_id)
                if from_account.balance >= amount:
                    from_account.balance -= amount
                    to_account.balance += amount
                    from_account.save()
                    to_account.save()
                    Transaction.objects.create(account=from_account, amount=amount, transaction_type='Transfer', to_account=to_account)
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
```