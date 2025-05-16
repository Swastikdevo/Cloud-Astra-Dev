```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@csrf_exempt
@login_required
def account_dashboard(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/account_dashboard.html', {'accounts': accounts})

    elif request.method == 'POST':
        action_type = request.POST.get('action')
        
        if action_type == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful.'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data.'}, status=400)

        elif action_type == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(id=form.cleaned_data['account_id'], user=request.user)
                
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful.'}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds.'}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
```