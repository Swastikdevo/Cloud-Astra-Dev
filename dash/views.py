```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@csrf_exempt
def bank_management_view(request):
    if request.method == 'POST':
        # Handle deposit
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return JsonResponse({'success': True, 'new_balance': account.balance})

        # Handle withdrawal
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return JsonResponse({'success': True, 'new_balance': account.balance})
                else:
                    return JsonResponse({'success': False, 'error': 'Insufficient funds'})

    else:
        # Display the account overview
        account = Account.objects.get(user=request.user)
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    return render(request, 'bank_management.html', {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    })
```