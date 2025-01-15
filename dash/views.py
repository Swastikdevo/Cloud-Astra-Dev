```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Account, Transaction
from .forms import CreateAccountForm, DepositForm, WithdrawForm

@login_required
def manage_account(request):
    accounts = Account.objects.filter(user=request.user)
    if request.method == 'POST':
        if 'create_account' in request.POST:
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.user = request.user
                account.save()
                return redirect('manage_account')

        elif 'deposit' in request.POST:
            form = DepositForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')
                return redirect('manage_account')

        elif 'withdraw' in request.POST:
            form = WithdrawForm(request.POST)
            if form.is_valid():
                account = form.cleaned_data['account']
                amount = form.cleaned_data['amount']
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')
                    return redirect('manage_account')

    else:
        create_form = CreateAccountForm()
        deposit_form = DepositForm()
        withdraw_form = WithdrawForm()

    return render(request, 'manage_account.html', {
        'accounts': accounts,
        'create_form': create_form,
        'deposit_form': deposit_form,
        'withdraw_form': withdraw_form,
    })

@require_POST
@login_required
def account_details(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    response_data = {
        'account_number': account.account_number,
        'balance': account.balance,
        'transactions': [{
            'amount': txn.amount,
            'transaction_type': txn.transaction_type,
            'created_at': txn.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for txn in transactions],
    }
    return JsonResponse(response_data)
```