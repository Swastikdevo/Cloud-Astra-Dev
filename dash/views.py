```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from .forms import DepositForm, WithdrawalForm, AccountCreationForm
from django.db import transaction

@login_required
def manage_account(request):
    user = request.user
    account = Account.objects.get(user=user)

    if request.method == 'POST':
        if 'deposit' in request.POST:
            deposit_form = DepositForm(request.POST)
            if deposit_form.is_valid():
                amount = deposit_form.cleaned_data['amount']
                with transaction.atomic():
                    account.balance += amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('manage_account')
        elif 'withdraw' in request.POST:
            withdrawal_form = WithdrawalForm(request.POST)
            if withdrawal_form.is_valid():
                amount = withdrawal_form.cleaned_data['amount']
                if account.balance >= amount:
                    with transaction.atomic():
                        account.balance -= amount
                        account.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='withdrawal')
                    return redirect('manage_account')
                else:
                    return JsonResponse({'error': 'Insufficient funds'}, status=400)
        elif 'create_account' in request.POST:
            account_creation_form = AccountCreationForm(request.POST)
            if account_creation_form.is_valid():
                new_account = account_creation_form.save(commit=False)
                new_account.user = user
                new_account.save()
                return redirect('manage_account')

    else:
        deposit_form = DepositForm()
        withdrawal_form = WithdrawalForm()
        account_creation_form = AccountCreationForm()

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdrawal_form': withdrawal_form,
        'account_creation_form': account_creation_form,
    }
    return render(request, 'bank/manage_account.html', context)
```