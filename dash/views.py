```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@csrf_exempt
def manage_account(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                return JsonResponse({'message': 'Deposit successful!', 'new_balance': account.balance})

        elif request.POST.get('action') == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                    return JsonResponse({'message': 'Withdrawal successful!', 'new_balance': account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds!'}, status=400)

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()
        account = Account.objects.get(user=request.user)

    return render(request, 'bank/manage_account.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'account_balance': account.balance
    })
```