```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@csrf_exempt
@login_required
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(user=request.user)
        return render(request, 'bank/account_overview.html', {'accounts': accounts})

    elif request.method == 'POST':
        action = request.POST.get('action')

        if action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account_id = form.cleaned_data['account_id']
                account = Account.objects.get(id=account_id, user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'success': True, 'message': 'Deposit successful!'}, status=200)

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account_id = form.cleaned_data['account_id']
                account = Account.objects.get(id=account_id, user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdraw')
                    return JsonResponse({'success': True, 'message': 'Withdrawal successful!'}, status=200)
                else:
                    return JsonResponse({'success': False, 'message': 'Insufficient funds!'}, status=400)

        return JsonResponse({'success': False, 'message': 'Invalid action or form data!'}, status=400)
```