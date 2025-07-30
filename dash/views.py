```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Transaction
from .forms import CreateAccountForm, DepositForm, WithdrawForm

@login_required
def manage_account(request):
    user = request.user
    account = Account.objects.filter(owner=user).first()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.owner = user
                account.save()
                messages.success(request, "Account created successfully!")
                return redirect('manage_account')

        elif action == 'deposit':
            form = DepositForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                messages.success(request, "Deposit successful!")
                return redirect('manage_account')

        elif action == 'withdraw':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                if amount <= account.balance:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    messages.success(request, "Withdrawal successful!")
                else:
                    messages.error(request, "Insufficient funds!")
                return redirect('manage_account')
    
    # Prepare forms
    create_account_form = CreateAccountForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    context = {
        'account': account,
        'create_account_form': create_account_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    }

    return render(request, 'manage_account.html', context)
```