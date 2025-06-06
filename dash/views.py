```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

@login_required
@require_http_methods(["GET", "POST"])
def manage_account(request):
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST) if 'deposit' in request.POST else None
        withdraw_form = WithdrawForm(request.POST) if 'withdraw' in request.POST else None
        
        if deposit_form and deposit_form.is_valid():
            account = Account.objects.get(user=request.user)
            amount = deposit_form.cleaned_data['amount']
            account.balance += amount
            account.save()

            # Record the transaction
            Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
            return JsonResponse({'success': True, 'message': 'Deposit successful.', 'new_balance': account.balance})

        elif withdraw_form and withdraw_form.is_valid():
            account = Account.objects.get(user=request.user)
            amount = withdraw_form.cleaned_data['amount']
            if amount <= account.balance:
                account.balance -= amount
                account.save()

                # Record the transaction
                Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                return JsonResponse({'success': True, 'message': 'Withdrawal successful.', 'new_balance': account.balance})
            else:
                return JsonResponse({'success': False, 'message': 'Insufficient funds.'})

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    account = Account.objects.get(user=request.user)
    return render(request, 'manage_account.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'balance': account.balance,
    })
```