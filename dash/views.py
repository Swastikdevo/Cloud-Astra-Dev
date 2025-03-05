```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'accounts/manage_account.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')
        account_id = request.POST.get('account_id')
        account = Account.objects.get(id=account_id)

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                account.balance += amount
                account.save()
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})

        elif action == 'withdraw':
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    Transaction.objects.create(account=account, amount=-amount, transaction_type='Withdrawal')
                    account.balance -= amount
                    account.save()
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient balance!'})

        return JsonResponse({'status': 'error', 'message': 'Invalid action or form data.'})
```