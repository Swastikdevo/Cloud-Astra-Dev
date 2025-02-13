```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import TransferForm, WithdrawalForm, DepositForm

@login_required
@csrf_exempt
def account_management(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'account_management.html', {'accounts': accounts})
    
    elif request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(pk=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid deposit data'})

        elif action == 'withdrawal':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                account = Account.objects.get(pk=form.cleaned_data['account_id'])
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid withdrawal data'})

        elif action == 'transfer':
            form = TransferForm(request.POST)
            if form.is_valid():
                source_account = Account.objects.get(pk=form.cleaned_data['source_account_id'])
                target_account = Account.objects.get(pk=form.cleaned_data['target_account_id'])
                amount = form.cleaned_data['amount']
                
                if source_account.balance >= amount:
                    source_account.balance -= amount
                    target_account.balance += amount
                    source_account.save()
                    target_account.save()
                    Transaction.objects.create(account=source_account, amount=amount, transaction_type='Transfer Out')
                    Transaction.objects.create(account=target_account, amount=amount, transaction_type='Transfer In')
                    return JsonResponse({'status': 'success', 'message': 'Transfer successful'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds for transfer'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid transfer data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
```