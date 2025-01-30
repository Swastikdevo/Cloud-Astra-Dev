```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(['GET', 'POST'])
def manage_account(request):
    if request.method == 'GET':
        accounts = Account.objects.filter(owner=request.user)
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        return render(request, 'bank/manage_account.html', {
            'accounts': accounts,
            'deposit_form': deposit_form,
            'withdrawal_form': withdrawal_form,
        })

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = deposit_form.cleaned_data['account']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'status': 'success', 'message': 'Deposit successful!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid deposit form!'})

        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                account = withdrawal_form.cleaned_data['account']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'status': 'success', 'message': 'Withdrawal successful!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Insufficient funds!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid withdrawal form!'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request!'})
```