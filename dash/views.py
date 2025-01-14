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
    """View to handle account management including deposits and withdrawals."""
    if request.method == 'POST':
        # Handle deposit
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                account.balance += amount
                account.save()

                transaction = Transaction(account=account, amount=amount, transaction_type='deposit')
                transaction.save()

                return JsonResponse({'success': 'Deposit successful!', 'new_balance': account.balance})
        
        # Handle withdrawal
        elif 'withdraw' in request.POST:
            withdraw_form = WithdrawForm(request.POST)
            if withdraw_form.is_valid():
                amount = withdraw_form.cleaned_data['amount']
                account = Account.objects.get(user=request.user)
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()

                    transaction = Transaction(account=account, amount=-amount, transaction_type='withdrawal')
                    transaction.save()

                    return JsonResponse({'success': 'Withdrawal successful!', 'new_balance': account.balance})
                else:
                    return JsonResponse({'error': 'Insufficient funds!'}, status=400)

    else:
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    return render(request, 'account/manage_account.html', {
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
        'current_balance': Account.objects.get(user=request.user).balance,
    })
```