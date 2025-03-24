```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm

@login_required
def manage_account(request):
    user_account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                user_account.balance += amount
                user_account.save()

                Transaction.objects.create(
                    account=user_account,
                    amount=amount,
                    transaction_type='Deposit',
                    description='Deposit made'
                )

                return redirect('account_overview')

        elif 'withdraw' in request.POST:
            form = WithdrawalForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= user_account.balance:
                    user_account.balance -= amount
                    user_account.save()

                    Transaction.objects.create(
                        account=user_account,
                        amount=amount,
                        transaction_type='Withdrawal',
                        description='Withdrawal made'
                    )
                    return redirect('account_overview')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()

    return render(request, 'manage_account.html', {
        'account': user_account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form
    })
```