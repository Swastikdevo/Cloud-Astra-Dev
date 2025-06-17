```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
@require_http_methods(["GET", "POST"])
def account_management(request):
    user_account = Account.objects.get(user=request.user)
    
    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        withdrawal_form = WithdrawalForm(request.POST)

        if 'deposit' in request.POST and deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            user_account.balance += amount
            user_account.save()
            Transaction.objects.create(
                account=user_account,
                amount=amount,
                transaction_type='Deposit'
            )
            return redirect('account_management')

        elif 'withdraw' in request.POST and withdrawal_form.is_valid():
            amount = withdrawal_form.cleaned_data['amount']
            if amount <= user_account.balance:
                user_account.balance -= amount
                user_account.save()
                Transaction.objects.create(
                    account=user_account,
                    amount=amount,
                    transaction_type='Withdrawal'
                )
                return redirect('account_management')
            else:
                withdrawal_form.add_error('amount', 'Insufficient balance')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
    
    transactions = Transaction.objects.filter(account=user_account).order_by('-created_at')

    context = {
        'user_account': user_account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'transactions': transactions,
    }

    return render(request, 'bank/account_management.html', context)
```