```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm, AccountCreationForm

@login_required
def manage_account(request):
    try:
        account = Account.objects.get(user=request.user)

        if request.method == 'POST':
            if 'deposit' in request.POST:
                form = DepositForm(request.POST)
                if form.is_valid():
                    amount = form.cleaned_data['amount']
                    account.balance += amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='Deposit')
                    messages.success(request, 'Deposit successful!')
                    return redirect('manage_account')

            elif 'withdraw' in request.POST:
                form = WithdrawForm(request.POST)
                if form.is_valid():
                    amount = form.cleaned_data['amount']
                    if amount > account.balance:
                        messages.error(request, 'Insufficient funds.')
                    else:
                        account.balance -= amount
                        account.save()
                        Transaction.objects.create(account=account, amount=amount, transaction_type='Withdrawal')
                        messages.success(request, 'Withdrawal successful!')
                        return redirect('manage_account')

        else:
            deposit_form = DepositForm()
            withdraw_form = WithdrawForm()

    except Account.DoesNotExist:
        messages.error(request, 'Account not found.')
        return redirect('create_account')

    context = {
        'account': account,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }
    return render(request, 'bank/manage_account.html', context)

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('manage_account')
    else:
        form = AccountCreationForm()

    return render(request, 'bank/create_account.html', {'form': form})
```